from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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
    mocker.patch("app.actions.get_clients", return_value=clients)

    response = client.get("/client")

    assert response.status_code == 200
    assert response.json() == clients

def test_get_client(mocker):
    """
        Cas passant (retorune un client)
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
    mocker.patch("app.actions.get_client", return_value=db_client)

    response = client.get("/client/" + str(db_client['id_client']))

    assert response.status_code == 200
    assert response.json() == db_client

def test_get_client_error_404(mocker):
    """
        Cas non passant (le client n'a pas été trouvé)
    """
    db_client = None
    mocker.patch("app.actions.get_client", return_value=db_client)

    response = client.get("/client/1")

    assert response.status_code == 404
