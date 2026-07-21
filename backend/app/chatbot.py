from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, User, Conversation, Message, Company
from app.schemas import ChatMessage
import google.generativeai as genai
import jwt
import os

router = APIRouter()

def get_current_user(token: str, db: Session):
    """Decode token and get user"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"]
        )
        user = db.get(User, payload["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired!")
    except:
        raise HTTPException(status_code=401, detail="Invalid token!")


@router.post("/chat")
def chat(
    data: ChatMessage,
    token: str,
    db: Session = Depends(get_db)
):
    # Step 1: Verify user
    user = get_current_user(token, db)
    
    # Step 2: Get or create conversation
    if data.conversation_id:
        conversation = db.get(Conversation, data.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found!")
    else:
        conversation = Conversation(
            user_id=user.id,
            title=data.message[:50]
        )
        db.add(conversation)
        db.commit()
    
    # Step 3: Get previous messages for context
    previous_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).all()
    
    # Step 4: Build conversation history for AI
    history = []

    # Add company system prompt FIRST (if company_id provided)
    if data.company_id:
        company = db.get(Company, data.company_id)
        if company:
            history.append(f"system: {company.system_prompt}")

    for msg in previous_messages:
        history.append(f"{msg.role}: {msg.content}")
    history.append(f"user: {data.message}")
    full_context = "\n".join(history)
    
    # Step 5: Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=data.message
    )
    db.add(user_message)
    
    # Step 6: Send to Gemini with history
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(full_context)
    ai_response = response.text
    
    # Step 7: Save AI response
    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response
    )
    db.add(ai_message)
    db.commit()
    
    # Step 8: Return response
    return {
        "conversation_id": conversation.id,
        "user_message": data.message,
        "ai_response": ai_response
    }

@router.get("/conversations")
def get_conversations(token: str, db: Session = Depends(get_db)):
    
    # Step 1: Verify user
    user = get_current_user(token, db)
    
    # Step 2: Get all conversations
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).all()
    
    # Step 3: Return list
    return {
        "conversations": [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at
            }
            for c in conversations
        ]
    }
@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int, token: str, db: Session = Depends(get_db)):
    
    # Step 1: Verify user
    user = get_current_user(token, db)
    
    # Step 2: Get messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()
    
    # Step 3: Return messages
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }
@router.post("/public-chat")
def public_chat(data: ChatMessage, db: Session = Depends(get_db)):
    # Step 1: Company must exist
    company = db.get(Company, data.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found!")

    # Step 2: Get or create conversation
    if data.conversation_id:
        conversation = db.get(Conversation, data.conversation_id)
    else:
        conversation = Conversation(
            company_id=company.id,
            title=data.message[:50]
        )
        db.add(conversation)
        db.commit()

    # Step 3: Get chat history
    previous_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).all()

    # Step 4: Build context with company personality
    history = [f"system: {company.system_prompt}"]
    for msg in previous_messages:
        history.append(f"{msg.role}: {msg.content}")
    history.append(f"user: {data.message}")
    full_context = "\n".join(history)

    # Step 5: Save user message
    db.add(Message(conversation_id=conversation.id, role="user", content=data.message))

    # Step 6: Ask Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(full_context)
    ai_response = response.text

    # Step 7: Save AI reply
    db.add(Message(conversation_id=conversation.id, role="assistant", content=ai_response))
    db.commit()

    # Step 8: Return response
    return {
        "conversation_id": conversation.id,
        "ai_response": ai_response
    }