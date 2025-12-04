from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.rag.rag_chain import get_rag_chain
from app.rag.vectordb import get_vector_db
from typing import List, Optional

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[str] = []

# Store conversation history (in production, use Redis or a database)
conversation_memory = {}

@router.post("/message")
def chat_message(chat: ChatMessage) -> ChatResponse:
    """
    AI Chatbot endpoint using RAG to answer questions about news articles.
    Uses retrieval-based responses from vectorDB for faster, more accurate answers.
    """
    try:
        vectordb = get_vector_db()
        
        # Get conversation ID or create new one
        conv_id = chat.conversation_id or f"conv_{len(conversation_memory)}"
        
        # Get conversation history
        history = conversation_memory.get(conv_id, [])
        
        # Search for relevant news articles
        docs = vectordb.similarity_search(chat.message, k=10)
        
        if not docs:
            answer = "I don't have any information about that topic in my current news database. Could you ask about Technology, Business, Science, Health, Sports, or Entertainment news?"
            sources = []
        else:
            # Build answer from retrieved documents
            articles_info = []
            sources = []
            seen_titles = set()
            seen_content = set()
            
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
                    
                    articles_info.append(article_text)
                    sources.append(source)
                
                if len(articles_info) >= 3:
                    break
            
            # Create a natural answer
            question_lower = chat.message.lower()
            
            if not articles_info:
                answer = "I found some articles but couldn't extract clear content. Could you try asking about a specific topic like AI, health, sports, or business?"
            elif any(word in question_lower for word in ["latest", "recent", "new", "what"]):
                answer = f"Here are the latest news articles I found:\n\n" + "\n\n".join(articles_info)
            elif "tell me about" in question_lower or "about" in question_lower:
                topic = chat.message.lower().replace("tell me about", "").replace("about", "").strip()
                answer = f"Here's what I found about {topic}:\n\n" + "\n\n".join(articles_info)
            else:
                answer = f"I found these relevant articles:\n\n" + "\n\n".join(articles_info)
            
            # Add helpful suffix
            if articles_info:
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
