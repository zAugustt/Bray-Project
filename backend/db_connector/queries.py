"""
Queries Module

This module provides queries that are used to communicate with the database in conjunction with the execute query
functions in the `DBConnector` class. The first argument of all queries should be a session object.

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University

Date:
    November 2024
"""

# from .models import Sensor, Event, DeviceData, DeviceInfo, DeviceTrendInfo
from .models import Event, DeviceInfo, DeviceData
from mqtt_client.sensor_event import SensorEvent
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import List
import logging


def create_tables(session):
    """
    Creates the schema in the database if not already present.

    Args:
        session (_type_): Session object. See module header.
    """
    from .models import Base
    Base.metadata.create_all(session.bind)

def flatten_data(sensor_event: SensorEvent):
    """
    Flattens data for use in database

    Args:
        sensor_event (SensorEvent): Event that contains torqueData
    Returns:
        flattened_torque_data: list of db compatible torque data
        record_numbers: list of packet numbers
        record_lengths: list of how long each packet is
    """
    logging.debug("Flattening data")
    # Transform sensor data to be compatible with db
    flattened_torque_data: List[int] = []
    record_numbers: List[int] = []
    record_lengths: List[int] = []

    if sensor_event.torqueData:
        for i, seq in enumerate(sensor_event.torqueData):
            if seq is not None:
                flattened_torque_data.extend(seq)
                record_lengths.append(len(seq))
                record_numbers.append(i + 1)
            else:
                record_lengths.append(0)
                record_numbers.append(-1)

    return (flattened_torque_data, record_numbers, record_lengths)

def add_sensor_event(session, sensor_event: SensorEvent):
    """
    Adds a sensor event to the database. SensorEvent is initialized with default data.

    Args:
        session (_type_): Session object. See module header.
        sensor_event (SensorEvent): Event that will be added to database
    """
    logging.info("Attempting to add sensor event")
    # Create device trend info entity
    device_trend_info = DeviceTrendInfo(
        strokeTime = sensor_event.strokeTime,
        maxTorque = sensor_event.maxTorque,
        temperature = sensor_event.temperature,
        batteryVoltage = sensor_event.batteryVoltage,
    )

    # Transform sensor data to be compatible with db
    flattened_torque_data, record_numbers, record_lengths = flatten_data(sensor_event)

    # Create device data entity
    device_data = DeviceData(
        lastTorqueBeforeSleep = sensor_event.lastTorqueBeforeSleep,
        firstTorqueAfterSleep = sensor_event.firstTorqueAfterSleep,
        recordNumbers = record_numbers,
        recordLengths = record_lengths,
        torqueData = flattened_torque_data,
        hiddenDataIndices = sensor_event.hiddenDataIndices,
        typeOfStroke = sensor_event.typeOfStroke,
        dataRecordPayloadCRCs = sensor_event.dataPacketPayloadCRCs,
        calculatedDataRecordPayloadCRCs = sensor_event.calculatedDataPacketPayloadCRCs,
        eventRecordPayloadCRC = sensor_event.eventSummaryPayloadCRC,
        calculatedEventRecordPayloadCRC = sensor_event.calculatedEventSummaryPayloadCRC,
        heartbeatRecordPayloadCRC = sensor_event.heartbeatRecordPayloadCRC,
        calculatedHeartbeatRecordPayloadCRC = sensor_event.calculatedHeartbeatRecordPayloadCRC,
    )

    # Create device info entity
    device_info = DeviceInfo(
        firmwareVersion = sensor_event.fwVersion,
        pwaRevision = sensor_event.pwaVersion,
        serialNumber = sensor_event.serialNumber,
        deviceType = sensor_event.deviceType,
        deviceLocation = sensor_event.deviceLocation,
        diagnostic = sensor_event.diagnostic,
        openValveCount = sensor_event.openValveCount,
        closeValveCount = sensor_event.closeValveCount,
    )

    # Create sensor entity if not exists
    sensor: Sensor = session.query(Sensor).filter_by(devEUI=sensor_event.devEUI).first()
    if sensor is None:
        sensor = Sensor(devEUI = sensor_event.devEUI)

    # Create event entity
    event = Event(
        timestamp=datetime(
            sensor_event.year,
            sensor_event.month,
            sensor_event.day,
            hour=sensor_event.hour,
            minute=sensor_event.minute,
            second=sensor_event.second,
        ),
        deviceInfo = device_info,
        deviceData = device_data,
        deviceTrendInfo = device_trend_info,
        sensor = sensor,
        isStreaming = sensor_event.isStreaming,
    )

    # Add session to db (also adds other entities)
    session.add(event)

def get_sensors(session):
    """
    Returns a list of sensors.

    Args:
        session (_type_): Session object. See module header.

    Returns:
        List[Sensor]: List of sensors containing `Sensor` objects.
    """
    return session.scalars(select(Sensor)
                           .options(joinedload(Sensor.events))  # Add entity property for Sensor to improve lookup times
                           ).unique().all()

def get_events(session, sensor_id: int):
    """
    Returns a list of events for a sensor.

    Args:
        session (_type_): Session object. See module header.
        sensor_id (int): ID of sensor.

    Returns:
        List[Event]: List of events containing `Event` objects.
    """
    return session.scalars(select(Event)
                           .filter_by(deviceinfoid=sensor_id)
                           #.options(joinedload(Event.DeviceData))
                           ).all()

def get_event(session, sensor_id: int, event_id: int):
    """
    Returns an event containing all event data.

    Args:
        session (_type_): Session object. See module header.
        sensor_id (int): ID of sensor.
        event_id (int): ID of event.

    Returns:
        Event: Event object containing all event information.
    """
    return session.scalars(select(Event)
                           .filter_by(id=event_id, sensorID=sensor_id)
                           .options(joinedload(Event.deviceInfo),
                                    joinedload(Event.deviceData),
                                    joinedload(Event.deviceTrendInfo))
                           ).first()

def get_device_events(session, sensor_id: int):
    """
    Returns a list of events for a sensor.

    Args:
        session (_type_): Session object. See module header.
        sensor_id (int): ID of sensor.

    Returns:
        List[Event]: List of events containing `Event` objects.
    """
    return session.scalars(select(Event)
                           .filter_by(deviceInfoID=sensor_id)
                           #.options(joinedload(Event.DeviceData))
    ).all()

def getDevInfo(session):
    """
    Retrieves all device information from the database.

    Args:
        session (_type_): Session object.

    Returns:
        List[DeviceInfo]: List of DeviceInfo objects.
    """
    return session.scalars(select(DeviceInfo)).all()

def getDevData(session, sensorName: str):
    """
    Retrieves device data for a specific sensor.

    Args:
        session (_type_): Session object.
        sensorName (str): Name of the sensor.

    Returns:
        List[DeviceData]: List of DeviceData objects associated with the sensor.
    """
    return session.scalars(
        select(DeviceData)
        .join(DeviceInfo, DeviceData.id == DeviceInfo.id)
        .filter(DeviceInfo.sensorName == sensorName)
    ).all()

def getEvents(session, sensorName: str):
    """
    Retrieves all events for a specific sensor.

    Args:
        session (_type_): Session object.
        sensorName (str): Name of the sensor.

    Returns:
        List[Event]: List of Event objects associated with the sensor.
    """
    return session.scalars(
        select(Event)
        .join(DeviceInfo, Event.deviceInfoID == DeviceInfo.id)
        .filter(DeviceInfo.sensorName == sensorName)
    ).all()

def getEvent(session, sensorName: str, eventId: int):
    """
    Retrieves a specific event for a sensor by event ID.

    Args:
        session (_type_): Session object.
        sensorName (str): Name of the sensor.
        eventId (int): ID of the event.

    Returns:
        Event: Event object matching the criteria.
    """
    return session.scalars(
        select(Event)
        .join(DeviceInfo, Event.deviceInfoID == DeviceInfo.id)
        .filter(DeviceInfo.sensorName == sensorName, Event.id == eventId)
    ).first()