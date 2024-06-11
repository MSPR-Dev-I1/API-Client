from pydantic import BaseModel

class ClientBase(BaseModel):
    """
        Classe interface base Client
    """
    id_client: int
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
