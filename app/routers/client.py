from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import actions, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Client])
async def get_clients(database: Session = Depends(get_db)):
    """
        Retourne tous les clients
    """
    db_clients = actions.get_clients(database)

    return db_clients

@router.get("/{id_client}", response_model=schemas.Client)
async def get_client(id_client: int, database: Session = Depends(get_db)):
    """
        Retourne le client trouvé par son id
    """
    db_client = actions.get_client(id_client, database)

    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return db_client
