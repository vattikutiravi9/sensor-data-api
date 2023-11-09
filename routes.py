from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from schemas import SensorData, StatisticResponse
from database import SensorDataModel, get_db
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter()

valid_reading_types = {"temperature", "humidity"}


@router.get("/")
def get_home():
    return {"message": "Welcome to the Sensor-data API"}


@router.post("/sensor-data", response_model=SensorData)
async def post_sensor_data(data: SensorData, db: Session = Depends(get_db)):
    # Convert reading_type to lowercase
    data.reading_type = data.reading_type.lower()
    # validate the reading type
    if data.reading_type not in valid_reading_types:
        raise HTTPException(status_code=400, detail="Enter a valid reading type")
    try:
        # Save the data in the database
        db_data = SensorDataModel(**data.model_dump())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database connection error")


@router.get("/sensor-data/", response_model=List[StatisticResponse])
async def get_sensor_data(
        sensor_ids: List[int] = Query(...),
        metrics: List[str] = Query(None),  # None means optional, can be omitted
        start_date: datetime = Query(None),
        end_date: datetime = Query(None),
        db: Session = Depends(get_db)
):
    try:
        # Validate sensor_ids
        actual_sensor_ids = {ids[0] for ids in db.query(SensorDataModel.sensor_id)
                                                 .filter(SensorDataModel.sensor_id.in_(sensor_ids)).distinct()}
        for sensor_id in sensor_ids:
            if sensor_id not in actual_sensor_ids:
                raise HTTPException(status_code=400, detail=f"Sensor ID {sensor_id} is not valid")

        # Validate the query parameters
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        if metrics:
            metrics = [metric.lower() for metric in metrics]
            if set(metrics) - valid_reading_types:
                raise HTTPException(status_code=400, detail="Enter a valid metric")
        # If no date range is specified, default to the latest data(last 7 days)
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        if not end_date:
            end_date = datetime.utcnow()

        # Base query
        query = db.query(
            SensorDataModel.sensor_id,
            SensorDataModel.reading_type,
            func.min(SensorDataModel.reading_value).label('min'),
            func.max(SensorDataModel.reading_value).label('max'),
            func.avg(SensorDataModel.reading_value).label('avg')
        ).filter(
            SensorDataModel.sensor_id.in_(sensor_ids),
            SensorDataModel.timestamp >= start_date,
            SensorDataModel.timestamp <= end_date
        )

        # Filter by metrics if specified
        if metrics:
            query = query.filter(SensorDataModel.reading_type.in_(metrics))

        # Group by sensor_id and reading_type to calculate statistics
        query = query.group_by(SensorDataModel.sensor_id, SensorDataModel.reading_type)

        # Execute the query
        results = query.all()

        # Format the results
        formatted_results = []
        for result in results:
            formatted_result = {
                "sensor_id": result.sensor_id,
                "reading_type": result.reading_type,
                "min": result.min,
                "max": result.max,
                "avg": result.avg
            }
            formatted_results.append(formatted_result)

        return formatted_results
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database connection error")
