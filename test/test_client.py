from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""Cas passant
    """
def test_get_client():
    get_client = {"Hello": "Client"}
    response = client.get("/client")
    assert response.status_code == 200
    assert response.json() == get_client