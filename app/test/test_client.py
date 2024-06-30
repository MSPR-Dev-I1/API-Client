from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pytest
from app.main import app
from app import models, actions
from app.models import Base
from app.routers.client import verify_authorization

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

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client",headers=headers)

    assert response.status_code == 200
    assert response.json() == clients

def test_get_clients_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client",headers=headers)

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

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/" + str(db_client['id_client']),headers=headers)

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

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1",headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Client not found'}

def test_get_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1",headers=headers)

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

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.post("/client", json=new_client,headers=headers)

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

def test_post_client_error_422(mocker):
    """
        Cas non passant (des informations du client sont manquants)
    """
    new_client = {
        "nom": "test",
        "adresse": "9 rue de la Monnaie",
        "code_postal": "59000",
        "ville": "Lille"
    }

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.post("/client", json=new_client,headers=headers)

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

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.post("/client", json=new_client,headers=headers)

    assert response.status_code == 500

def test_delete_client(mocker):
    """
        Cas passant (retourne l'id du client supprimé)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    mocker.patch("app.actions.get_client", return_value=db_client)
    mocker.patch("sqlalchemy.orm.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.delete("/client/" + str(db_client.id_client),headers=headers)

    assert response.status_code == 200
    assert response.json() == {"deleted": db_client.id_client}

def test_delete_client_error_404(mocker):
    """
        Cas non passant (le client n'est pas trouvée)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.delete("/client/1",headers=headers)

    assert response.status_code == 404

def test_delete_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    mocker.patch("app.actions.get_client", return_value=db_client)
    mocker.patch("sqlalchemy.orm.Session.delete", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.delete("/client/1",headers=headers)

    assert response.status_code == 500

def test_patch_client(mocker):
    """
        Cas passant (retourne le client mis à jour)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    client_updated = {
        "nom": "test2",
        "prenom": "test2"
    }
    mocker.patch("app.actions.get_client", return_value=db_client)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.patch("/client/" + str(db_client.id_client),
                            json=client_updated,headers=headers)

    assert response.status_code == 200
    assert response.json()["nom"] == client_updated["nom"]
    assert response.json()["prenom"] == client_updated["prenom"]

def test_patch_client_error_404(mocker):
    """
         Cas non passant (le client n'est pas trouvé)
    """
    client_updated = {
        "nom": "test2",
        "prenom": "test2"
    }
    mocker.patch("app.actions.get_client", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.patch("/client/1", json=client_updated,headers=headers)

    assert response.status_code == 404

def test_patch_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    client_updated = {
        "nom": "test2",
        "prenom": "test2"
    }
    mocker.patch("app.actions.get_client", return_value=db_client)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.patch("/client/" + str(db_client.id_client),
                            json=client_updated,headers=headers)

    assert response.status_code == 500

def test_get_informations_de_contact(mocker):
    """
        Cas passant (retourne l'email du client)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    mocker.patch("app.actions.get_client", return_value=db_client)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/" + str(db_client.id_client) + "/informations_de_contact",
                          headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()['email'] == db_client.email

def test_get_informations_de_contact_error_404(mocker):
    """
        Cas non passant (ne trouve pas le client)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1/informations_de_contact",headers=headers)

    assert response.status_code == 404

def test_get_informations_de_contact_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.actions.get_client", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1/informations_de_contact",headers=headers)

    assert response.status_code == 500

def test_get_nom_prenom_client(mocker):
    """
        Cas passant (retourne l'email du client)
    """
    db_client = models.Client(
        id_client=1,
        nom="test",
        prenom="test",
        email="test.test@ecoles-epsi.net",
        adresse="9 rue de la Monnaie",
        code_postal="59000",
        ville="Lille"
    )
    mocker.patch("app.actions.get_client", return_value=db_client)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/" + str(db_client.id_client) + "/nom_prenom_client",
                          headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()['prenom'] == db_client.prenom
    assert response.json()['nom'] == db_client.nom


def test_get_nom_prenom_client_error_404(mocker):
    """
        Cas non passant (ne trouve pas le client)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1/nom_prenom_client",headers=headers)

    assert response.status_code == 404

def test_get_nom_prenom_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.actions.get_client", side_effect=Exception("Connection error"))

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    headers = {"token": "None"}
    response = client.get("/client/1/nom_prenom_client",headers=headers)

    assert response.status_code == 500

@pytest.mark.parametrize("token", ["test_token"])
def test_post_deconnexion(mocker, token):
    """
        Test de la route deconnexion
    """
    mock_publisher = mocker.MagicMock()
    mock_publisher_topic = mocker.MagicMock()
    mocker.patch("app.message.create_publisher", return_value=mock_publisher)
    mocker.patch("google.cloud.pubsub_v1.PublisherClient.topic_path",
        return_value=mock_publisher_topic)
    mocker.patch("google.cloud.pubsub_v1.PublisherClient.publish", return_value=None)

    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}

    response = client.post("/client/deconnexion", json={"token": token})

    assert response.status_code == 200
    assert response.json() == {"token": "revoked"}


def test_verify_authorization_no_header():
    """Test when authorization header is missing"""
    with pytest.raises(HTTPException) as exc_info:
        verify_authorization(None)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authorization header missing"

def test_verify_authorization_invalid_token(mocker):
    """Test when the token is invalid"""
    mocker.patch("app.routers.client.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.client.requests.post")
    mock_response.return_value.status_code = 401
    mock_response.return_value.json.return_value = {"validation": False}

    with pytest.raises(HTTPException) as exc_info:
        verify_authorization("invalid-token")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Failed to send data to external API"

def test_verify_authorization_unauthorized(mocker):
    """Test when the token is unauthorized"""
    mocker.patch("app.routers.client.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.client.requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"validation": False}

    with pytest.raises(HTTPException) as exc_info:
        verify_authorization("unauthorized-token")
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "UnAuthorized"

def test_verify_authorization_success(mocker):
    """Test when the token is valid"""
    mocker.patch("app.routers.client.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.client.requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"validation": True}

    try:
        verify_authorization("valid-token")
    except HTTPException:
        pytest.fail("verify_authorization raised HTTPException unexpectedly!")
