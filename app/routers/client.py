from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import actions, schemas, models

router = APIRouter()

@router.get("", response_model=List[schemas.Client])
async def get_clients(database: Session = Depends(get_db)):
    """
        Retourne tous les clients
    """
    try:
        db_clients = actions.get_clients(database)

        return db_clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_client}", response_model=schemas.Client)
async def get_client(id_client: int, database: Session = Depends(get_db)):
    """
        Retourne le client trouvé par son id
    """
    try:
        db_client = actions.get_client(id_client, database)

        if db_client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        return db_client
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post("", response_model=schemas.Client, status_code=201)
async def post_client(client: schemas.ClientCreate, database: Session = Depends(get_db)):
    """
        Créer un nouveau client
    """
    try:
        new_client = models.Client(
            nom=client.nom,
            prenom=client.prenom,
            email=client.email,
            adresse=client.adresse,
            code_postal=client.code_postal,
            ville=client.ville,
        )
        db_client = actions.create_client(new_client, database)

        return db_client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
