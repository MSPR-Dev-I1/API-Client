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
