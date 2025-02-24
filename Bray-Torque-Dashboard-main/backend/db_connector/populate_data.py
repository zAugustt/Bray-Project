from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sensor, Event, DeviceInfo, DeviceTrendInfo, DeviceData
from datetime import datetime
from os import getenv

print("Starting populate_data.py script")

# Replace with your actual database URL
DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv("POSTGRES_USER", "test_user"),
    getenv("POSTGRES_PASSWORD", None),
    getenv("POSTGRES_HOST", "localhost"),
    getenv("POSTGRES_PORT", 5432),
    getenv("POSTGRES_DB", "test")
)

print(f"Connecting to database at {DATABASE_URL}")

try:
    # Create an engine and a session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Database connection established")

    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    print("Tables created")

    # Sample data
    sensor = Sensor(devEUI="00-14-22-01-23-45")

    device_info = DeviceInfo(
        firmwareVersion="1.0.0",
        pwaRevision="A",
        serialNumber="SN123456",
        deviceType="TypeA",
        deviceLocation="LocationA",
        diagnostic=0,
        openValveCount=10,
        closeValveCount=10
    )

    device_trend_info = DeviceTrendInfo(
        strokeTime=100,
        maxTorque=200,
        temperature=25,
        batteryVoltage=3.7
    )

    device_data = DeviceData(
        lastTorqueBeforeSleep=150,
        firstTorqueAfterSleep=160,
        recordNumbers=[1, 2, 3],
        recordLengths=[10, 20, 30],
        torqueData=[100, 200, 300],
        hiddenDataIndices=[0, 1],
        typeOfStroke=1,
        dataRecordPayloadCRCs=[123, 456],
        calculatedDataRecordPayloadCRCs=[123, 456],
        eventRecordPayloadCRC=789,
        calculatedEventRecordPayloadCRC=789,
        heartbeatRecordPayloadCRC=101112,
        calculatedHeartbeatRecordPayloadCRC=101112
    )

    event = Event(
        timestamp=datetime.now(),
        isStreaming=True,
        deviceInfo=device_info,
        deviceData=device_data,
        deviceTrendInfo=device_trend_info,
        sensor=sensor
    )

    # Add and commit the sample data
    session.add(sensor)
    session.add(event)
    session.commit()

    print("Sample data added successfully!")
except Exception as e:
    print(f"An error occurred: {e}")