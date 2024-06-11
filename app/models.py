from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey

# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """
        Classe Model de base SqlAlchemy
    """

# pylint: disable=too-few-public-methods
class Client(Base):
    """
        Classe Model de la table client
    """
    __tablename__ = "client"

    id_client: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(200))
    adresse: Mapped[str] = mapped_column(String(300))
    code_postal: Mapped[str] = mapped_column(String(10))
    ville: Mapped[str] = mapped_column(String(50))

    commandes: Mapped[List["CommandeClient"]] \
        = relationship(back_populates="client", cascade="all, delete-orphan")

# pylint: disable=too-few-public-methods
class CommandeClient(Base):
    """
        Classe Model de la table commande_client
    """
    __tablename__ = "commande_client"

    id_commande: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id_client"))

    client: Mapped["Client"] = relationship(back_populates="commandes")
