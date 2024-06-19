from sqlalchemy.orm import Session
from app import models, schemas

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

def create_client(client: models.Client, database: Session):
    """
        Créer et retourne le client
    """
    database.add(client)
    database.commit()
    database.refresh(client)
    return client

def delete_client(client: models.Client, database: Session):
    """
        Supprime un client de la base de données
    """
    database.delete(client)
    database.commit()

def update_client(db_client: models.Client, client: schemas.ClientUpdate, database: Session):
    """
        Met à jour les données du client
    """
    client_data = client.model_dump(exclude_unset=True)
    for key, value in client_data.items():
        setattr(db_client, key, value)

    database.commit()

    return db_client
