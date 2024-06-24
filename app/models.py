from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

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
