import pytest
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_connector import DBConnector
from db_connector.models import Base, Sensor, AuxSensor, AuxSensorData
from db_connector.queries import (
    create_tables,
    add_aux_sensor_data,
    get_aux_sensors,
    get_aux_sensor_data,
)

PG_DB_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv("POSTGRES_USER", "test_user"),
    getenv("POSTGRES_PASSWORD", None),
    getenv("POSTGRES_HOST", "localhost"),
    getenv("POSTGRES_PORT", 5432),
    getenv("POSTGRES_DB", "test")
)

# Setup a PostgreSQL test database for testing
@pytest.fixture(scope="function")
def db_session():
    # Connect to your local PostgreSQL database
    engine = create_engine(PG_DB_URI)
    Base.metadata.create_all(engine)  # Create tables in the local database
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def clean_db(db_session):
    # Truncate all tables after each test
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture(scope="function")
def db_connector():
    return DBConnector()


def test_create_tables(db_session):
    """Test that tables are created successfully."""
    tables = db_session.bind.table_names()
    assert "sensors" in tables
    assert "aux_sensors" in tables
    assert "aux_sensor_data" in tables


def test_add_aux_sensor_data(db_session):
    """Test adding auxiliary sensor data."""
    from mqtt_client.aux_sensor_event import AuxSensorEvent

    # Create a mock AuxSensorEvent
    aux_sensor_event = AuxSensorEvent()
    aux_sensor_event.aux_sensor_id = 1
    aux_sensor_event.timestamp = "2025-04-27 12:00:00"
    aux_sensor_event.co2_percentage = 42.5

    # Add the data
    add_aux_sensor_data(db_session, aux_sensor_event)

    # Verify the data was added
    aux_sensor = db_session.query(AuxSensor).filter_by(id=1).first()
    assert aux_sensor is not None

    aux_sensor_data = db_session.query(AuxSensorData).filter_by(aux_sensor_id=1).first()
    assert aux_sensor_data is not None
    assert aux_sensor_data.value == 42.5


def test_get_aux_sensors(db_session):
    """Test retrieving auxiliary sensors."""
    # Add a sensor
    aux_sensor = AuxSensor(id=1)
    db_session.add(aux_sensor)
    db_session.commit()

    # Retrieve sensors
    sensors = get_aux_sensors(db_session)
    assert len(sensors) == 1
    assert sensors[0].id == 1


def test_get_aux_sensor_data(db_session):
    """Test retrieving auxiliary sensor data."""
    # Add a sensor and data
    aux_sensor = AuxSensor(id=1)
    db_session.add(aux_sensor)
    aux_sensor_data = AuxSensorData(aux_sensor_id=1, timestamp="2025-04-27 12:00:00", value=42.5)
    db_session.add(aux_sensor_data)
    db_session.commit()

    # Retrieve data
    data = get_aux_sensor_data(db_session, sensor_id=1)
    assert len(data) == 1
    assert data[0].value == 42.5


def test_execute_query(db_connector, db_session):
    """Test executing a query with DBConnector."""
    def mock_query(session):
        aux_sensor = AuxSensor(id=1)
        session.add(aux_sensor)

    db_connector.execute_query(mock_query)
    aux_sensor = db_session.query(AuxSensor).filter_by(id=1).first()
    assert aux_sensor is not None


def test_execute_query_readonly(db_connector, db_session):
    """Test executing a read-only query with DBConnector."""
    # Add a sensor
    aux_sensor = AuxSensor(id=1)
    db_session.add(aux_sensor)
    db_session.commit()

    def mock_query(session):
        return session.query(AuxSensor).filter_by(id=1).first()

    result = db_connector.execute_query_readonly(mock_query)
    assert result is not None
    assert result.id == 1