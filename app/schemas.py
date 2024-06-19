from typing import Union
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

class ClientUpdate(BaseModel):
    """
        Classe interface Client Update
    """
    nom: Union[str, None] = None
    prenom: Union[str, None] = None
    email: Union[str, None] = None
    adresse: Union[str, None] = None
    code_postal: Union[str, None] = None
    ville: Union[str, None] = None
