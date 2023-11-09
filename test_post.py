from fastapi.testclient import TestClient
from main import app
from datetime import datetime
client = TestClient(app)


def test_post_sensor_data_ok():
    response = client.post("/sensor-data", json={
        "sensor_id": 1,
        "reading_type": "Humidity",
        "reading_value": 100,
        "timestamp": datetime.now().isoformat()
    })
    assert response.status_code == 200
    assert response.json()["sensor_id"] == 1
    assert response.json()["reading_value"] == 100


def test_post_sensor_data_400():
    response = client.post("/sensor-data", json={
        "sensor_id": 1,
        "reading_type": "invalid",
        "reading_value": 100,
        "timestamp": datetime.now().isoformat()
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Enter a valid reading type"
