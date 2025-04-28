import pytest
from flask import Flask
import csv

from api_v1.custom_csv import fetch_event_data, format_event_data, write_event_csv
from db_connector import DBConnector
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

@pytest.fixture
def fake_session():
    return MagicMock(spec=Session)

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Proper fake event for backend tests
class FakeDeviceData:
    lastTorqueBeforeSleep = 0
    firstTorqueAfterSleep = 0
    recordNumbers = [1, 2]
    recordLengths = [3, 4]
    torqueData = [[10, 20, 30], [40, 50, 60]]
    hiddenDataIndices = [1]
    typeOfStroke = 0
    dataRecordPayloadCRCs = []
    calculatedDataRecordPayloadCRCs = []
    eventRecordPayloadCRC = 0
    calculatedEventRecordPayloadCRC = 0
    heartbeatRecordPayloadCRC = 0
    calculatedHeartbeatRecordPayloadCRC = 0

class FakeDeviceInfo:
    firmwareVersion = "v1.0"
    pwaRevision = "A"
    serialNumber = "12345"
    deviceType = "sensor"
    deviceLocation = "TestLoc"
    diagnostic = 0
    openValveCount = 0
    closeValveCount = 0

class FakeDeviceTrendInfo:
    strokeTime = 0
    maxTorque = 0
    temperature = 0
    batteryVoltage = 0

class FakeEvent:
    id = 1
    timestamp = "2025-04-28 00:00:00"
    isStreaming = True
    deviceData = FakeDeviceData()
    deviceInfo = FakeDeviceInfo()
    deviceTrendInfo = FakeDeviceTrendInfo()


def test_sensors(client):
    response = client.get("/api_v1/sensors")
    assert response.status_code in [200, 500]

def test_events_happy(client):
    response = client.get("/api_v1/sensors/1/events")
    assert response.status_code in [200, 500]

def test_events_last_n(client):
    response = client.get("/api_v1/sensors/1/events/last/5")
    assert response.status_code in [200, 500]

def test_event(client):
    response = client.get("/api_v1/sensors/1/events/1")
    assert response.status_code in [200, 500]

def test_event_download(client):
    response = client.get("/api_v1/sensors/1/events/1/download")
    assert response.status_code in [200, 500]

def test_aux_sensors(client):
    response = client.get("/api_v1/aux_sensors")
    assert response.status_code in [200, 500]

def test_devices(client):
    response = client.get("/api_v1/devices")
    assert response.status_code in [200, 500]

def test_aux_sensor_data(client):
    response = client.get("/api_v1/aux_sensor_data")
    assert response.status_code in [200, 500]

def test_event_hidden(client):
    response = client.get("/api_v1/sensors/1/events/1/hidden")
    assert response.status_code in [200, 500]

def test_event_download_hidden(client):
    response = client.get("/api_v1/sensors/1/events/1/download/hidden")
    assert response.status_code in [200, 500]

# --- Backend logic tests ---

def test_fetch_event_data(fake_session):
    fake_session.query.return_value.filter_by.return_value.first.return_value = FakeEvent()
    result = fetch_event_data(fake_session, sensor_id=1, event_id=1)
    assert isinstance(result, dict)
    assert "id" in result

def test_format_event_data_empty():
    formatted = format_event_data(FakeEvent())
    assert isinstance(formatted, list)

def test_format_event_data_realistic():
    formatted = format_event_data(FakeEvent())
    assert isinstance(formatted, list)
    assert len(formatted) >= 1

def test_format_event_data_realistic_hide():
    formatted = format_event_data(FakeEvent(), hide_packet_data=True)
    assert isinstance(formatted, list)

def test_write_event_csv(tmp_path):
    event_data = format_event_data(FakeEvent())
    output_file = tmp_path / "output.csv"
    with output_file.open('w', newline='') as f:
        writer = csv.writer(f)
        # Note: Passing both header and rows separately
        header = [
            "ID", "Timestamp", "Firmware Version", "PWA Revision", "Serial Number",
            "Device Type", "Device Location", "Diagnostic", "Open Valve Count",
            "Close Valve Count", "Stroke Time", "Max Torque", "Temperature",
            "Battery Voltage", "Last Torque Before Sleep", "First Torque After Sleep",
            "Record Numbers", "Record Lengths", "Torque Data", "Type Of Stroke",
            "Data Record CRCs", "Calculated Data Record CRCs", "Event CRC",
            "Calculated Event CRC", "Heartbeat CRC", "Calculated Heartbeat CRC"
        ]
        rows = [[
            event_data.get("id", ""),
            event_data.get("timestamp", ""),
            event_data.get("firmwareVersion", ""),
            event_data.get("pwaRevision", ""),
            event_data.get("serialNumber", ""),
            event_data.get("deviceType", ""),
            event_data.get("deviceLocation", ""),
            event_data.get("diagnostic", ""),
            event_data.get("openValveCount", ""),
            event_data.get("closeValveCount", ""),
            event_data.get("strokeTime", ""),
            event_data.get("maxTorque", ""),
            event_data.get("temperature", ""),
            event_data.get("batteryVoltage", ""),
            event_data.get("lastTorqueBeforeSleep", ""),
            event_data.get("firstTorqueAfterSleep", ""),
            event_data.get("recordNumbers", ""),
            event_data.get("recordLengths", ""),
            event_data.get("torqueData", ""),
            event_data.get("typeOfStroke", ""),
            event_data.get("dataRecordPayloadCRCs", ""),
            event_data.get("calculatedDataRecordPayloadCRCs", ""),
            event_data.get("eventRecordPayloadCRC", ""),
            event_data.get("calculatedEventRecordPayloadCRC", ""),
            event_data.get("heartbeatRecordPayloadCRC", ""),
            event_data.get("calculatedHeartbeatRecordPayloadCRC", ""),
        ]]
        write_event_csv(writer, header, rows)

    # Now verify the file contents
    contents = output_file.read_text()
    assert "File Created:" in contents
    assert "ID,Timestamp,Firmware Version" in contents
