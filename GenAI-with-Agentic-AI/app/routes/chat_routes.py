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
    AI Chatbot endpoint using RAG to answer questions about news articles
    """
    try:
        # Get RAG chain
        rag_chain = get_rag_chain()
        vectordb = get_vector_db()
        
        # Get conversation ID or create new one
        conv_id = chat.conversation_id or f"conv_{len(conversation_memory)}"
        
        # Get conversation history
        history = conversation_memory.get(conv_id, [])
        
        # Build context from history
        context = "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history[-3:]])
        
        # Augment query with context if available
        query = chat.message
        if context:
            query = f"Previous conversation:\n{context}\n\nCurrent question: {chat.message}"
        
        # Use RAG chain to get answer
        try:
            # Try the new invoke API
            result = rag_chain.invoke(query)
            if isinstance(result, dict):
                answer = result.get("result", str(result))
            else:
                answer = str(result)
        except AttributeError:
            # Fallback to legacy __call__ if invoke doesn't exist
            result = rag_chain(query)
            answer = result.get("result", str(result))
        
        # Get source documents for context
        docs = vectordb.similarity_search(chat.message, k=3)
        sources = [doc.metadata.get("source", "Unknown") for doc in docs]
        
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
