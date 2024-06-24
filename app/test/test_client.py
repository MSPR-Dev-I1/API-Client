from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pytest
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

    response = client.delete("/client/" + str(db_client.id_client))

    assert response.status_code == 200
    assert response.json() == {"deleted": db_client.id_client}

def test_delete_client_error_404(mocker):
    """
        Cas non passant (le client n'est pas trouvée)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    response = client.delete("/client/1")

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

    response = client.delete("/client/1")

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

    response = client.patch("/client/" + str(db_client.id_client), json=client_updated)

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

    response = client.patch("/client/1", json=client_updated)

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

    response = client.patch("/client/" + str(db_client.id_client), json=client_updated)

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

    response = client.get("/client/" + str(db_client.id_client) + "/informations_de_contact")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()['email'] == db_client.email

def test_get_informations_de_contact_error_404(mocker):
    """
        Cas non passant (ne trouve pas le client)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    response = client.get("/client/1/informations_de_contact")

    assert response.status_code == 404

def test_get_informations_de_contact_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.actions.get_client", side_effect=Exception("Connection error"))

    response = client.get("/client/1/informations_de_contact")

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

    response = client.get("/client/" + str(db_client.id_client) + "/nom_prenom_client")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()['prenom'] == db_client.prenom
    assert response.json()['nom'] == db_client.nom


def test_get_nom_prenom_client_error_404(mocker):
    """
        Cas non passant (ne trouve pas le client)
    """
    mocker.patch("app.actions.get_client", return_value=None)

    response = client.get("/client/1/nom_prenom_client")

    assert response.status_code == 404

def test_get_nom_prenom_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.actions.get_client", side_effect=Exception("Connection error"))

    response = client.get("/client/1/nom_prenom_client")

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

    response = client.post("/client/deconnexion", json={"token": token})

    assert response.status_code == 200
    assert response.json() == {"token": "revoked"}
