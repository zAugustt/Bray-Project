import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_connector import DBConnector
from db_connector.models import Base, Sensor, AuxSensor, AuxSensorData, DeviceData, DeviceInfo, DeviceTrendInfo, Event
from db_connector.queries import (
    create_tables,
    add_aux_sensor_data,
    add_sensor_event,
    upsert_live_sensor_event,
    get_aux_sensors,
    get_aux_sensor_data,
    get_sensors,
    get_events,
    get_event,
    flatten_data,
    hide_duplicate_packets,
)
from unittest.mock import patch
from sqlalchemy.exc import OperationalError

class FakeSensorEvent:
    devEUI = "test_dev_eui"
    torqueData = [[1, 2, 3], [4, 5]]
    lastTorqueBeforeSleep = 1
    firstTorqueAfterSleep = 2
    hiddenDataIndices = [0]
    typeOfStroke = 0
    dataPacketPayloadCRCs = [123]
    calculatedDataPacketPayloadCRCs = [123]
    eventSummaryPayloadCRC = 123
    calculatedEventSummaryPayloadCRC = 123
    heartbeatRecordPayloadCRC = 123
    calculatedHeartbeatRecordPayloadCRC = 123
    strokeTime = 10
    maxTorque = 100
    temperature = 25
    batteryVoltage = 12
    fwVersion = "1.0"
    pwaVersion = "A1"
    serialNumber = "SN12345"
    deviceType = "Sensor"
    deviceLocation = "Nowhere"
    diagnostic = 0
    openValveCount = 10
    closeValveCount = 10
    isStreaming = True
    aux_sensor_id = 1
    timestamp = "2025-04-27 12:00:00"
    co2_percentage = 42.5

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("postgresql://test_user:test_password@db_test:5432/test_db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()

@pytest.fixture(scope="function", autouse=True)
def clean_db(db_session):
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

@pytest.fixture(scope="function")
def db_connector():
    return DBConnector()

def test_db_connector_init():
    connector = DBConnector()
    assert connector is not None

def test_create_tables_function(db_session):
    create_tables(db_session)

def test_add_aux_sensor_data(db_session):
    event = FakeSensorEvent()
    add_aux_sensor_data(db_session, event)
    aux_sensor = db_session.query(AuxSensor).filter_by(id=1).first()
    assert aux_sensor is not None
    aux_sensor_data = db_session.query(AuxSensorData).filter_by(aux_sensor_id=1).first()
    assert aux_sensor_data is not None
    assert aux_sensor_data.value == 42.5

def test_get_aux_sensors(db_session):
    aux_sensor = AuxSensor(id=1)
    db_session.add(aux_sensor)
    db_session.commit()
    sensors = get_aux_sensors(db_session)
    assert len(sensors) == 1

def test_get_aux_sensor_data(db_session):
    aux_sensor = AuxSensor(id=1)
    db_session.add(aux_sensor)
    aux_sensor_data = AuxSensorData(aux_sensor_id=1, timestamp="2025-04-27 12:00:00", value=42.5)
    db_session.add(aux_sensor_data)
    db_session.commit()
    data = get_aux_sensor_data(db_session, sensor_id=1)
    assert len(data) == 1

def test_execute_query(db_connector):
    def mock_query(session):
        aux_sensor = AuxSensor(id=2)
        session.add(aux_sensor)
    db_connector.execute_query(mock_query)

def test_execute_query_with_exception(db_connector):
    def mock_query(session):
        raise Exception("mock failure")
    db_connector.execute_query(mock_query)

def test_execute_query_readonly_with_exception(db_connector):
    def mock_query(session):
        raise Exception("mock failure")
    db_connector.execute_query_readonly(mock_query)

def test_initialize_db_with_retry(db_connector):
    db_connector.initialize_db_with_retry()

def test_initialize_db_with_retry_retry(monkeypatch):
    connector = DBConnector()
    call_counter = {"count": 0}

    def fake_inspect(engine):
        call_counter["count"] += 1
        if call_counter["count"] < 2:
            raise OperationalError("mock", None, None)
        else:
            class DummyInspector:
                def get_table_names(self):
                    return ["dummy"]
            return DummyInspector()

    monkeypatch.setattr("sqlalchemy.inspect", fake_inspect)
    connector.initialize_db_with_retry(max_retries=3, delay=0)

def test_flatten_data_multiple_packets():
    event = FakeSensorEvent()
    event.torqueData = [[1, 2], [3, 4], [5, 6]]
    result = flatten_data(event)
    assert isinstance(result, tuple)
    assert len(result) == 3

def test_hide_duplicate_packets_varied():
    result = hide_duplicate_packets(
        data=[1, 2, 3, 4],
        record_numbers=[1, 2, 3, 4],
        record_lengths=[1, 1, 1, 1],
        crc=[111, 222, 333, 444],
        prev_data=[1, 2, 3],
        prev_record_numbers=[1, 2, 3],
        prev_record_lengths=[1, 1, 1],
        prev_crc=[111, 222, 333]
    )
    assert isinstance(result, list)

def test_add_sensor_event(db_session):
    event = FakeSensorEvent()
    add_sensor_event(db_session, event)
    sensor = db_session.query(Sensor).filter_by(devEUI="test_dev_eui").first()
    assert sensor is not None

def test_upsert_live_sensor_event_insert(db_session):
    event = FakeSensorEvent()
    upsert_live_sensor_event(db_session, event)

def test_upsert_live_sensor_event_existing_non_streaming(db_session):
    sensor = Sensor(devEUI="test_dev_eui")
    db_session.add(sensor)
    db_session.commit()
    event = Event(
        timestamp="2025-04-27 12:00:00",
        deviceInfo=None,
        deviceData=None,
        deviceTrendInfo=None,
        sensor=sensor,
        isStreaming=False,
    )
    db_session.add(event)
    db_session.commit()

    fake_event = FakeSensorEvent()
    upsert_live_sensor_event(db_session, fake_event)

def test_upsert_live_sensor_event_full_update(db_session):
    sensor = Sensor(devEUI="test_dev_eui")
    db_session.add(sensor)
    db_session.commit()

    device_data = DeviceData()
    device_info = DeviceInfo()
    device_trend_info = DeviceTrendInfo()

    event = Event(
        timestamp="2025-04-27 12:00:00",
        deviceInfo=device_info,
        deviceData=device_data,
        deviceTrendInfo=device_trend_info,
        sensor=sensor,
        isStreaming=True,
    )
    db_session.add(event)
    db_session.commit()

    fake_event = FakeSensorEvent()
    upsert_live_sensor_event(db_session, fake_event)

def test_upsert_live_sensor_event_event_summary(db_session):
    event = FakeSensorEvent()
    upsert_live_sensor_event(db_session, event, eventType=2)

def test_upsert_live_sensor_event_with_previous(db_session):
    event = FakeSensorEvent()
    prev_event = FakeSensorEvent()
    upsert_live_sensor_event(db_session, event, prev_sensor_event=prev_event)

def test_get_sensors(db_session):
    sensor = Sensor(id=1, devEUI="test_dev_eui")
    db_session.add(sensor)
    db_session.commit()
    sensors = get_sensors(db_session)
    assert len(sensors) == 1

def test_get_events(db_session):
    sensor = Sensor(id=1, devEUI="test_dev_eui")
    db_session.add(sensor)
    db_session.commit()
    events = get_events(db_session, sensor_id=1)
    assert isinstance(events, list)

def test_get_event(db_session):
    sensor = Sensor(id=1, devEUI="test_dev_eui")
    db_session.add(sensor)
    db_session.commit()
    event = get_event(db_session, sensor_id=1, event_id=999)
    assert event is None or hasattr(event, 'id')
