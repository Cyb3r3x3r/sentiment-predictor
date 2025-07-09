from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={"text": "I love this product!"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert isinstance(data["label"], str)
    assert isinstance(data["score"], float)
