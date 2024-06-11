from sqlalchemy.orm import Session
from app import models

def get_clients(database: Session):
    """
        Retourne la liste des clients
    """
    all_clients = database.query(models.Client)
    return all_clients
