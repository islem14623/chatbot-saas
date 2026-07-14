from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    company_id: Optional[int] = None

class CompanyCreate(BaseModel):
    name: str
    description: str
    system_prompt: str