from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.schemas import CompanyCreate
from app.chatbot import get_current_user

router = APIRouter()

@router.post("/")
def create_company(
    data: CompanyCreate,
    token: str,
    db: Session = Depends(get_db)
):
    # Step 1: Verify user
    user = get_current_user(token, db)
    
    # Step 2: Create company
    company = Company(
        name=data.name,
        description=data.description,
        system_prompt=data.system_prompt,
        owner_id=user.id
    )
    
    db.add(company)
    db.commit()
    
    return {
        "message": "Company created!",
        "company_id": company.id,
        "name": company.name
    }

@router.get("/")
def get_companies(token: str, db: Session = Depends(get_db)):
    
    # Step 1: Verify user
    user = get_current_user(token, db)
    
    # Step 2: Get companies
    companies = db.query(Company).filter(
        Company.owner_id == user.id
    ).all()
    
    return {
        "companies": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description
            }
            for c in companies
        ]
    }
