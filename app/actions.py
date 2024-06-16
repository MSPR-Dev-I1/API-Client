from sqlalchemy.orm import Session
from app import models

def get_clients(database: Session):
    """
        Retourne la liste des clients
    """
    all_clients = database.query(models.Client)
    return all_clients

def get_client(id_client: int, database: Session):
    """
        Retourne un client
    """
    client = database.query(models.Client).where(models.Client.id_client == id_client).first()
    return client
