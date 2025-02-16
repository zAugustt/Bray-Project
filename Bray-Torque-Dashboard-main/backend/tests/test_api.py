import pytest
from api_v1 import api_v1  # Import the app factory function from your app

# TODO :: Create db and populate
# TODO :: teardown db


def test_sensors(client):
    response = client.get("/api_v1/sensors")

    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 1


def test_events_happy(client):
    response = client.get("/api_v1/sensors/1/events")
    
    assert response.status_code == 200
    assert "event_datas" in response.json
    assert "batteryVoltages" in response.json
    assert "maxTorques" in response.json
    assert "strokeTimes" in response.json
    assert "temperatures" in response.json


@pytest.mark.parametrize("n_events,expected_n_events", [
    (0, 0),
    (2, 2),
])
def test_events_last_n(client, n_events, expected_n_events):
    response = client.get(f"/api_v1/sensors/1/events/last/{n_events}")
    
    assert response.status_code == 200
    assert "event_datas" in response.json
    assert "batteryVoltages" in response.json
    assert "maxTorques" in response.json
    assert "strokeTimes" in response.json
    assert "temperatures" in response.json
    assert len(response.json["batteryVoltages"]) == expected_n_events
    assert len(response.json["maxTorques"]) == expected_n_events
    assert len(response.json["strokeTimes"]) == expected_n_events
    assert len(response.json["temperatures"]) == expected_n_events


def test_event(client):
    response = client.get("/api_v1/sensors/1/events/1")
    
    assert response.status_code == 200
    assert "id" in response.json
    assert "timestamp" in response.json
    assert "firmwareVersion" in response.json
    assert "pwaRevision" in response.json
    assert "serialNumber" in response.json
    assert "deviceType" in response.json
    assert "deviceLocation" in response.json
    assert "diagnostic" in response.json
    assert "openValveCount" in response.json
    assert "closeValveCount" in response.json
    assert "strokeTime" in response.json
    assert "maxTorque" in response.json
    assert "temperature" in response.json
    assert "batteryVoltage" in response.json
    assert "lastTorqueBeforeSleep" in response.json
    assert "firstTorqueAfterSleep" in response.json
    assert "recordNumbers" in response.json
    assert "recordLengths" in response.json
    assert "torqueData" in response.json
    assert "typeOfStroke" in response.json
    assert "dataRecordPayloadCRCs" in response.json
    assert "calculatedDataRecordPayloadCRCs" in response.json
    assert "eventRecordPayloadCRC" in response.json
    assert "calculatedEventRecordPayloadCRC" in response.json
    assert "heartbeatRecordPayloadCRC" in response.json
    assert "calculatedHeartbeatRecordPayloadCRC" in response.json


def test_event_download(client):
    response = client.get("/api_v1/sensors/1/events/1/download")

    assert response.status_code == 200
    assert b"Not Implemented: event download" in response.data
