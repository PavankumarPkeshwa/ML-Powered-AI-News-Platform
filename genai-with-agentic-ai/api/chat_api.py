from fastapi import APIRouter, Query
from pydantic import BaseModel
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.rag_chain import get_rag_chain
from rag.vectordb import get_vector_db
from rag.llm import HuggingFaceAPILLM
from typing import List, Optional
import re
import logging

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# Initialize LLM for analytical questions
llm = None
logger = logging.getLogger(__name__)

def get_llm():
    """Initialize LLM lazily - uses HuggingFace Inference API (serverless)"""
    global llm
    if llm is None:
        # Check if we have HuggingFace token
        hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        
        if hf_token:
            logger.info("🔄 Initializing Llama 3.2 via HuggingFace API (serverless)...")
            logger.info(f"   Token: {hf_token[:10]}...")
            try:
                # Use HuggingFace Inference API - no download needed!
                llm = HuggingFaceAPILLM(
                    model_name="meta-llama/Llama-3.2-3B-Instruct:novita",
                    max_tokens=256,
                    temperature=0.7
                )
                logger.info("✅ Llama 3.2 API ready! (serverless, no downloads)")
            except Exception as e:
                logger.error(f"⚠️ Could not initialize HF API: {e}")
                logger.info("💡 Falling back to local Flan-T5...")
                from rag.llm import LocalLLM
                llm = LocalLLM(model_name="google/flan-t5-base", max_length=256)
                logger.info("✅ Flan-T5 local model ready!")
        else:
            logger.warning("⚠️ No HF_TOKEN found, using local Flan-T5-base")
            from rag.llm import LocalLLM
            llm = LocalLLM(model_name="google/flan-t5-base", max_length=256)
            logger.info("✅ Flan-T5 local model ready!")
    
    return llm

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[str] = []

# Store conversation history (in production, use Redis or a database)
conversation_memory = {}

def detect_query_type(message: str) -> tuple[str, str]:
    """
    Detect if the query is asking for:
    1. 'list' - Direct article listing (latest news, show me news, etc.)
    2. 'analytical' - Opinion/reasoning question (will X, why X, how X, should X)
    
    Returns: (query_type, category)
    """
    message_lower = message.lower()
    
    # Category detection
    categories = {
        'technology': ['tech', 'technology', 'ai', 'artificial intelligence', 'software', 'computer', 'app', 'digital'],
        'health': ['health', 'medical', 'disease', 'medicine', 'healthcare', 'doctor', 'hospital', 'wellness'],
        'business': ['business', 'economy', 'finance', 'market', 'stock', 'company', 'corporate'],
        'sports': ['sport', 'athlete', 'game', 'football', 'basketball', 'tennis', 'olympic'],
        'science': ['science', 'research', 'study', 'discovery', 'experiment', 'scientific'],
        'entertainment': ['entertainment', 'movie', 'music', 'celebrity', 'film', 'concert', 'show']
    }
    
    detected_category = None
    for category, keywords in categories.items():
        if any(keyword in message_lower for keyword in keywords):
            detected_category = category.capitalize()
            break
    
    # Query type detection
    # List queries - asking for articles/news directly
    list_patterns = [
        r'\b(latest|recent|new|top|show|give|list|display|what|tell).*(news|article|story|headline)',
        r'\b(what|show).*(news|article)',
        r'(latest|recent|new|top|show).*\b(in|about|on)',
        r'news (about|on|in|related to)',
    ]
    
    # Analytical queries - asking for opinions, explanations, reasoning
    analytical_patterns = [
        r'\b(will|can|could|would|should|may|might)',
        r'\b(why|how|explain|reason|because)',
        r'\b(impact|effect|consequence|result)',
        r'\b(think|believe|opinion|perspective)',
        r'\b(compare|difference|better|worse)',
        r'\b(future|predict|forecast)',
    ]
    
    is_list_query = any(re.search(pattern, message_lower) for pattern in list_patterns)
    is_analytical_query = any(re.search(pattern, message_lower) for pattern in analytical_patterns)
    
    # Determine query type
    if is_list_query and not is_analytical_query:
        query_type = 'list'
    elif is_analytical_query:
        query_type = 'analytical'
    else:
        # Default: if very short or simple, assume list; otherwise analytical
        query_type = 'list' if len(message.split()) <= 5 else 'analytical'
    
    return query_type, detected_category


@router.post("/message")
def chat_message(chat: ChatMessage) -> ChatResponse:
    """
    AI Chatbot endpoint with two modes:
    1. List mode: Shows top articles directly
    2. Analytical mode: Uses LLM to generate reasoned answers
    """
    try:
        vectordb = get_vector_db()
        
        # Get conversation ID or create new one
        conv_id = chat.conversation_id or f"conv_{len(conversation_memory)}"
        
        # Get conversation history
        history = conversation_memory.get(conv_id, [])
        
        # Detect query type and category
        query_type, detected_category = detect_query_type(chat.message)
        
        print(f"🔍 Query type: {query_type}, Category: {detected_category}")
        
        # Search for relevant news articles
        search_k = 10 if query_type == 'list' else 5
        
        # Build filter for category if detected
        filter_dict = None
        if detected_category:
            filter_dict = {"category": detected_category}
        
        # Perform search
        if filter_dict:
            docs = vectordb.similarity_search(chat.message, k=search_k, filter=filter_dict)
            # If no results with filter, try without filter
            if not docs:
                docs = vectordb.similarity_search(chat.message, k=search_k)
        else:
            docs = vectordb.similarity_search(chat.message, k=search_k)
        
        if not docs:
            answer = "I don't have any information about that topic in my current news database. Could you ask about Technology, Business, Science, Health, Sports, or Entertainment news?"
            sources = []
        else:
            # Build answer from retrieved documents
            articles_info = []
            sources = []
            seen_titles = set()
            seen_content = set()
            
            max_articles = 10 if query_type == 'list' else 3
            
            for doc in docs:
                title = doc.metadata.get("title", "").strip()
                content = doc.page_content.strip()
                
                # Skip if no meaningful title
                if not title or len(title) < 10:
                    continue
                
                # Skip duplicates by title (exact match)
                if title in seen_titles:
                    continue
                
                # Skip duplicates by content (first 150 chars as fingerprint)
                content_fingerprint = content[:150].lower().replace(' ', '')
                if content_fingerprint in seen_content:
                    continue
                
                # Filter out navigation/scraped HTML junk
                junk_indicators = [
                    "Latest AI Amazon Apps Biotech",
                    "Subscribe",
                    "Sign in",
                    "Click here",
                    len(content) < 100,  # Too short
                ]
                
                if any(indicator if isinstance(indicator, bool) else indicator in content[:150] 
                       for indicator in junk_indicators):
                    continue
                
                # Extract clean excerpt (first 2-3 sentences)
                sentences = [s.strip() + '.' for s in content.split('.') if len(s.strip()) > 30]
                if sentences:
                    excerpt = ' '.join(sentences[:2])[:280]
                else:
                    excerpt = content[:280]
                
                # Only add if we have meaningful, unique content
                if len(excerpt) > 80:
                    seen_titles.add(title)
                    seen_content.add(content_fingerprint)
                    
                    source = doc.metadata.get("source", "Unknown")
                    category = doc.metadata.get("category", "")
                    
                    article_text = f"📰 **{title}**"
                    if category:
                        article_text += f" _{category}_"
                    article_text += f"\n\n{excerpt}"
                    if not excerpt.endswith('.'):
                        article_text += "..."
                    
                    articles_info.append({
                        'formatted': article_text,
                        'title': title,
                        'content': content,
                        'category': category
                    })
                    sources.append(source)
                
                if len(articles_info) >= max_articles:
                    break
            
            # Generate answer based on query type
            if not articles_info:
                answer = "I found some articles but couldn't extract clear content. Could you try asking about a specific topic like AI, health, sports, or business?"
            
            elif query_type == 'list':
                # LIST MODE: Show articles directly
                formatted_articles = [article['formatted'] for article in articles_info]
                
                if detected_category:
                    answer = f"Here are the latest {detected_category} news articles:\n\n" + "\n\n".join(formatted_articles)
                else:
                    answer = f"Here are the latest news articles:\n\n" + "\n\n".join(formatted_articles)
                
                answer += f"\n\n📊 Showing {len(articles_info)} articles"
                answer += "\n💬 Would you like to know more about any specific topic?"
            
            else:
                # ANALYTICAL MODE: Use LLM to generate reasoned answer
                print("🤖 Using LLM for analytical response...")
                
                # Prepare context from articles (keep it short for small models)
                context_parts = []
                for i, article in enumerate(articles_info[:3], 1):  # Use only top 3 articles
                    # Extract key points (first 250 chars of content)
                    snippet = article['content'][:250].strip()
                    context_parts.append(f"Article {i} - {article['title']}:\n{snippet}")
                
                context = "\n\n".join(context_parts)
                
                # Check if we have HuggingFace token (indicates Llama model)
                import os
                hf_token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
                
                # Create prompt based on model type
                if hf_token:
                    # Llama 3.2 Instruct format - needs specific instruction formatting
                    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant that analyzes news articles and provides clear, informative answers. Use the provided news context to answer questions accurately and concisely.<|eot_id|><|start_header_id|>user<|end_header_id|>

Question: {chat.message}

Recent news context:
{context}

Please provide a clear, informative answer (2-4 sentences) based on the news articles above.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
                else:
                    # Flan-T5 format - simpler prompt
                    prompt = f"""Question: {chat.message}

Relevant news context:
{context}

Based on the news above, provide a clear and concise answer (2-3 sentences):"""
                
                # Get LLM response
                try:
                    model = get_llm()
                    llm_answer = model.invoke(prompt).strip()
                    
                    # Check if LLM answer is meaningful (not empty or too short)
                    if llm_answer and len(llm_answer) > 20:
                        # Format final answer with LLM response + article references
                        answer = f"🤔 **Analysis:**\n\n{llm_answer}\n\n"
                        answer += f"📚 **Related Articles:**\n\n"
                        
                        # Add top 3 article references
                        for article in articles_info[:3]:
                            answer += article['formatted'] + "\n\n"
                        
                        answer += "💬 Would you like to explore this topic further?"
                    else:
                        # LLM gave poor answer, use article-based response instead
                        print("⚠️ LLM answer too short, using article summary instead")
                        formatted_articles = [article['formatted'] for article in articles_info[:3]]
                        answer = f"Based on recent news, here's what I found:\n\n" + "\n\n".join(formatted_articles)
                        answer += "\n\n💬 Would you like to know more about any specific topic?"
                    
                except Exception as llm_error:
                    print(f"⚠️ LLM error: {llm_error}")
                    # Fallback to article listing if LLM fails
                    formatted_articles = [article['formatted'] for article in articles_info[:3]]
                    answer = f"Based on recent news, here's what I found:\n\n" + "\n\n".join(formatted_articles)
                    answer += "\n\n💬 Would you like to know more about any specific topic?"
        
        # Save to conversation history
        if conv_id not in conversation_memory:
            conversation_memory[conv_id] = []
        
        conversation_memory[conv_id].append({
            "user": chat.message,
            "assistant": answer
        })
        
        # Limit history to last 10 exchanges
        if len(conversation_memory[conv_id]) > 10:
            conversation_memory[conv_id] = conversation_memory[conv_id][-10:]
        
        return ChatResponse(
            response=answer,
            conversation_id=conv_id,
            sources=sources
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return ChatResponse(
            response=f"I'm sorry, I encountered an error: {str(e)}. Please try again.",
            conversation_id=chat.conversation_id or "error",
            sources=[]
        )


@router.delete("/conversation/{conversation_id}")
def clear_conversation(conversation_id: str):
    """
    Clear conversation history
    """
    if conversation_id in conversation_memory:
        del conversation_memory[conversation_id]
        return {"message": "Conversation cleared"}
    return {"message": "Conversation not found"}


@router.get("/health")
def chatbot_health():
    """
    Check if chatbot service is ready
    """
    try:
        vectordb = get_vector_db()
        return {
            "status": "healthy",
            "message": "Chatbot service is ready",
            "conversations": len(conversation_memory)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": str(e)
        }
