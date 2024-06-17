from pydantic import BaseModel

class ClientBase(BaseModel):
    """
        Classe interface base Client
    """
    nom: str
    prenom: str
    email: str
    adresse: str
    code_postal: str
    ville: str

class Client(ClientBase):
    """
        Classe interface Client
    """
    id_client: int

class ClientCreate(ClientBase):
    """
        Classe interface Client Create
    """
