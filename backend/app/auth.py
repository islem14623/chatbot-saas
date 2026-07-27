import jwt
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister

router = APIRouter()

@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    
    # Step 1: Check if email exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists!")

    # Step 1.5: Check password strength
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters!")
    
    # Step 2: Create user
    new_user = User(
        email=data.email,
        username=data.username
    )
    
    # Step 3: Hash password
    new_user.set_password(data.password)
    
    # Step 4: Save
    db.add(new_user)
    db.commit()
    
    # Step 5: Return
    return {
        "message": "User created successfully!",
        "user_id": new_user.id
    }


@router.post("/login")
def login(data: UserRegister, db: Session = Depends(get_db)):
    # Step 1: Find user and check password together
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.check_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password!")
    
    # Step 3: Create JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256"
    )
    
    # Step 4: Return token
    return {
        "message": "Login successful!",
        "token": token
    }