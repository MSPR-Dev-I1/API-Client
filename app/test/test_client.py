from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app import models, actions
from app.models import Base

client = TestClient(app)

def memory_engine():
    """
        Créer un engine sqlalchemy qui utilise la mémoire
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    database = scoped_session(session_factory)

    return database

def test_get_clients(mocker):
    """
        Cas passant (retourne la liste de client)
    """
    clients = [{
       "id_client": 1,
        "nom": "test",
        "prenom": "test",
        "email": "test.test@ecoles-epsi.net",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=clients)

    response = client.get("/client")

    assert response.status_code == 200
    assert response.json() == clients

def test_get_clients_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/client")

    assert response.status_code == 500

def test_get_client(mocker):
    """
        Cas passant (retourne un client)
    """
    db_client = {
       "id_client": 1,
        "nom": "test",
        "prenom": "test",
        "email": "test.test@ecoles-epsi.net",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_client
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/client/" + str(db_client['id_client']))

    assert response.status_code == 200
    assert response.json() == db_client

def test_get_client_error_404(mocker):
    """
        Cas non passant (le client n'a pas été trouvé)
    """
    db_client = None
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_client
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/client/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Client not found'}

def test_get_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/client/1")

    assert response.status_code == 500

def test_post_client(mocker):
    """
        Cas passant (retourne le client avec un id)
    """
    new_client = {
        "nom": "test",
        "prenom": "test",
        "email": "test.test@ecoles-epsi.net",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }
    db_client = models.Client(
        id_client=1,
        nom=new_client['nom'],
        prenom=new_client['prenom'],
        email=new_client['email'],
        adresse=new_client['adresse'],
        code_postal=new_client['code_postal'],
        ville=new_client['ville']
    )

    mocker.patch("app.actions.create_client", return_value=db_client)

    response = client.post("/client", json=new_client)

    assert response.status_code == 201

def test_action_create_client():
    """
        Test unitaire de la function create client
    """
    database = memory_engine()
    new_client = models.Client(
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )

    db_client = actions.create_client(new_client, database)
    assert isinstance(db_client, models.Client)
    assert db_client.id_client is not None

def test_post_client_error_422():
    """
        Cas non passant (des informations du client sont manquants)
    """
    new_client = {
        "nom": "test",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }

    response = client.post("/client", json=new_client)

    assert response.status_code == 422

def test_post_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    new_client = {
        "nom": "test",
        "prenom": "test",
        "email": "test.test@ecoles-epsi.net",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.post("/client", json=new_client)

    assert response.status_code == 500
