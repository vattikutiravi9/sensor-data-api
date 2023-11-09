from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

client = TestClient(app)


def test_get_sensor_data_temperature():
    # Assuming you have a sensor with ID 1 and it has temperature data
    response = client.get(
        "/sensor-data/",
        params={
            "sensor_ids": [1],
            "metrics": ["Temperature"],
            "start_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "end_date": datetime.utcnow().isoformat(),
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert 'avg' in data[0]
    assert data[0]['reading_type'] == 'temperature'


def test_get_sensor_data_no_metrics_provided():
    # Test to ensure it handles the case where no metrics are provided
    response = client.get(
        "/sensor-data/",
        params={
            "sensor_ids": [1],
            "start_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "end_date": datetime.utcnow().isoformat(),
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]['sensor_id'] == 1


def test_get_sensor_data_no_dates_provided():
    # Test to ensure it handles the case where no dates are provided
    response = client.get(
        "/sensor-data/",
        params={
            "sensor_ids": [1],
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]['sensor_id'] == 1


def test_get_sensor_data_invalid_metrics_provided():
    # Test to ensure it handles the case where no metrics are provided
    response = client.get(
        "/sensor-data/",
        params={
            "sensor_ids": [1],
            "metrics": ["Temperature", "invalid"],
            "start_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "end_date": datetime.utcnow().isoformat(),
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Enter a valid metric"


def test_get_sensor_data_invalid_date_range():
    # Test to ensure it handles an invalid date range correctly
    response = client.get(
        "/sensor-data/",
        params={
            "sensor_ids": [1],
            "metrics": ["Temperature"],
            "start_date": datetime.utcnow().isoformat(),
            "end_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        }
    )
    assert response.status_code == 400
    assert response.json()['detail'] == "End date must be after start date"
