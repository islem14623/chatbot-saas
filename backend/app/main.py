from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router  # ADD THIS
import app.models  # Import models so tables are created
from app.chatbot import router as chat_router
from app.companies import router as companies_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chatbot SaaS API",
    version="1.0.0",
    description="AI Chatbot SaaS for businesses"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api/auth")  # ADD THIS
app.include_router(chat_router, prefix="/api/chat")
app.include_router(companies_router, prefix="/api/companies")
@app.get("/")
def home():
    return {
        "message": "🤖 Chatbot SaaS API",
        "status": "running",
        "version": "1.0.0"
    }

