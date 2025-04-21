from os import getenv
from sqlalchemy.orm import Session
from models import Base, Event, DeviceInfo, DeviceData
from sqlalchemy import create_engine
from datetime import datetime
import random

# Database connection string (update with your actual database URI)
PG_DB_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv("POSTGRES_USER", "test_user"),
    getenv("POSTGRES_PASSWORD", None),
    getenv("POSTGRES_HOST", "localhost"),
    getenv("POSTGRES_PORT", 5432),
    getenv("POSTGRES_DB", "test")
)
# Create the database engine
engine = create_engine(PG_DB_URI)

# Generate test data
def generate_test_data():
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Start a session
    with Session(engine) as session:
        # Generate DeviceInfo entries
        devices = []
        for i in range(5):  # Generate 5 devices
            device = DeviceInfo(
                sensorname=f"Sensor_{i+1}",
                serialnumber=f"SN{i+1:05d}",
                devicetype=random.choice(["Type A", "Type B", "Type C"]),
                devicelocation=random.choice(["Building 1", "Building 2", "Building 3"]),
            )
            devices.append(device)
            session.add(device)

        # Commit devices to get their IDs
        session.commit()

        # Generate DeviceData and Event entries
        for device in devices:
            # Generate DeviceData
            device_data = DeviceData(
                measurementdata=[random.uniform(0.0, 100.0) for _ in range(10)]  # 10 random float values
            )
            session.add(device_data)
            session.commit()  # Commit to get the ID of device_data

            # Generate Event
            event = Event(
                deviceinfoid=device.id,
                devicedataid=device_data.id,
                timestamp=datetime.now(),
            )
            session.add(event)

        # Commit all changes
        session.commit()

if __name__ == "__main__":
    generate_test_data()