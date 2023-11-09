from sqlalchemy import Column, Integer, DateTime, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./weather_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SensorDataModel(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    reading_type = Column(String, nullable=False)
    reading_value = Column(Float, nullable=False)
