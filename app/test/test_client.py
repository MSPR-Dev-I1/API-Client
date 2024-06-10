import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_client(mocker):
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
    mocker.patch("app.actions.get_clients", return_value=clients)

    response = client.get("/client")

    assert response.status_code == 200
    assert response.json() == clients

def test_get_client_error_500():
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    with unittest.mock.patch("app.actions.get_clients") as mocked_test_connection:
        mocked_test_connection.side_effect = Exception("Connection error")

        response = client.get("/client")

        assert response.status_code == 500
        assert response.json() == {"detail": "Connection failed: Connection error"}
