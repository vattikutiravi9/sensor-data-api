# Sensor Data API

Sensor Data API is a FastAPI application that receives and queries weather sensor data, such as temperature, humidity. The API allows for posting sensor data to a database and querying the data with various filters and statistical computations.

## Features

- Post sensor data to the database.
- Query sensor data with filters for sensor IDs, metrics and date ranges.
- Calculates average, minimum and maximum  of the specified metrics.
- Data validation and exception handling.
- Unit tests for the API endpoints.

## Getting Started

### Prerequisites

Before running the application, you need to have the following installed:

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository to your local machine:

```bash
https://github.com/vattikutiravi9/sensor-data-api.git
cd sensor-data-api
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up the database:

The application is configured to use SQLite by default.

4. Run the application:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot reloading during development.

### Usage

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs` or `http://localhost:8000/docs`. This documentation provides an interactive UI to test the API endpoints.

#### Posting Sensor Data

To post sensor data, send a POST request to `/sensor-data` with the following JSON payload:

```json
{
  "sensor_id": 1,
  "reading_type": "Temperature",
  "reading_value": 22.5,
  "timestamp": "2023-11-08T21:45:27.665000"
}
```

#### Querying Sensor Data

To query sensor data, send a GET request to `/sensor-data/` with the required query parameters.
```
      params={
            "sensor_ids": [1],
            "metrics": ["Temperature"],
            "start_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "end_date": datetime.utcnow().isoformat(),
        }
```
### Running Tests

To run the tests, use the following command:

```bash
pytest
```

For the time being separate test database is not configured. But for production use ensure that you have a test database configured.

### LIVE API
You can access this API with the instance of this app deployed in GCP cloud run with the below link
```
https://sample-oo6b5z3xfq-nn.a.run.app/docs
```
