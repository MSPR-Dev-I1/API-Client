import os
from typing import List
import requests
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app import actions, schemas, models, message


router = APIRouter()

def verify_authorization(token: str = Header(None)):
    """
        The function is to be called before the controlers.
        It reads the token in the header and verify it with the APi Authentication
    """
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    url = os.getenv("AUTHURL")
    key = os.getenv("SERVICEKEY")
    payload = {"token":token,"service_key":key}
    response = requests.post(f"http://{url}/authentification/validation_token",
                             json=payload, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Failed to send data to external API")
    validation = response.json().get("validation")
    if validation is None or validation is not True:
        raise HTTPException(status_code=403, detail="UnAuthorized")


@router.get("", response_model=List[schemas.Client], tags=["client"])
async def get_clients(database: Session = Depends(get_db), _ = Depends(verify_authorization)):
    """
        Retourne tous les clients
    """
    try:
        db_clients = actions.get_clients(database)

        return db_clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_client}", response_model=schemas.Client, tags=["client"])
async def get_client(id_client: int, database: Session = Depends(get_db),
                     _ = Depends(verify_authorization)):
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

@router.post("", response_model=schemas.Client, status_code=201, tags=["client"])
async def post_client(client: schemas.ClientCreate,
                      database: Session = Depends(get_db),
                      _ = Depends(verify_authorization)):
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

@router.delete("/{id_client}", tags=["client"])
async def delete_client(id_client: int,
                        database: Session = Depends(get_db),
                        _ = Depends(verify_authorization)):
    """
        Supprime un client
    """
    try:
        db_client = actions.get_client(id_client, database)
        if db_client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        actions.delete_client(db_client, database)

        return {"deleted": id_client}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.patch("/{id_client}", response_model=schemas.Client, tags=["client"])
async def patch_client(id_client: int,
    client: schemas.ClientUpdate,
    database: Session = Depends(get_db),
    _ = Depends(verify_authorization)):
    """
        Met à jour les donénes du client
    """
    try:
        db_client = actions.get_client(id_client, database)
        if db_client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        db_client = actions.update_client(db_client, client, database)

        return db_client
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_client}/informations_de_contact/",
    response_model=schemas.InformationsContact, tags=["client"])
async def informations_contact(id_client: int,
                               database: Session = Depends(get_db),
                               _ = Depends(verify_authorization)):
    """
        Retourne les informations de contact d'un client
    """
    try:
        db_client = actions.get_client(id_client, database)
        if db_client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        informations_de_contact = schemas.InformationsContact(
            email=db_client.email,
        )

        return informations_de_contact
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_client}/nom_prenom_client/",
    response_model=schemas.NomPrenomClient, tags=["client"])
async def nom_prenom(id_client: int,
                     database: Session = Depends(get_db),
                     _ = Depends(verify_authorization)):
    """
        Retourne le nom et prénom du client
    """
    try:
        db_client = actions.get_client(id_client, database)
        if db_client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        nom_prenom_client = schemas.NomPrenomClient(
            nom=db_client.nom,
            prenom=db_client.prenom,
        )

        return nom_prenom_client
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post('/deconnexion', tags=["client"])
async def deconnexion(token: schemas.TokenClient):
    """
        Revoque le token de l'utilisateur
    """
    message.revoke_token_message(token)
    return {"token": "revoked"}


@router.get('/demo', tags=["client"])
async def demo(_ = Depends(verify_authorization)):
    return {"Demo": "MSPR"}