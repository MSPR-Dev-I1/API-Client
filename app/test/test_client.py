from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_client():
    """
        Cas passant
    """
    get_client = {"Hello": "Client"}
    response = client.get("/client")
    assert response.status_code == 200
    assert response.json() == get_client
