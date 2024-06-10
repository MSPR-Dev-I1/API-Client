from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import actions, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Client])
async def get_client(database: Session = Depends(get_db)):
    """
        Retourne tous les clients
    """
    try:
        db_clients = actions.get_clients(database)
        return db_clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
