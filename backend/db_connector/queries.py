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

from .models import Sensor, Event, DeviceData, DeviceInfo, DeviceTrendInfo
from mqtt_client.sensor_event import SensorEvent
# from mqtt_client.aux_sensor_data import AuxSensorData
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


def hide_duplicate_packets(data: int, record_numbers: int, record_lengths: int, crc: List[int],
                           prev_data: int, prev_record_numbers: int, prev_record_lengths: int, prev_crc: List[int]):
    """
    Finds duplicate packets from 2 events
    Args:
        data (int): list of flattened torque data for the event
        record_numbers (List[int]): list of record numbers for the event
        record_lengths (List[int]): list of record lengths for the event
        crc (List[int]): list of crcs for the event
        prev_data (List[int]): list of flattened torque data for the previous event
        prev_record_numbers (List[int]): list of record numbers for the previous event
        prev_record_lengths (List[int]): list of record lengths for the previous event
        prev_crc (List[int]): list of crcs for the previous event

    Returns:
        (List): List of integers representing the packet numbers to hide
    """
    logging.info("Attempting to locate duplicate packets")

    duplicate_packets = []
    # Start at the last packet and go backward
    index = len(record_lengths) - 1
    prev_index = len(prev_record_lengths) - 1

    # Loop while both indices are valid
    while index >= 0 and prev_index >= 0:
        start       = sum(record_lengths[:index])
        end         = start + record_lengths[index]

        prev_start  = sum(prev_record_lengths[:prev_index])
        prev_end    = prev_start + prev_record_lengths[prev_index]

        # If data and CRC match, store the packet number
        if ((data[start:end] == prev_data[prev_start:prev_end]) and (crc[index] == prev_crc[prev_index])):
            duplicate_packets.insert(0, record_numbers[index])
        else:
            break

        index      -= 1
        prev_index -= 1
    return duplicate_packets


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


def upsert_live_sensor_event(session, sensor_event: SensorEvent, eventType: int = -1, prev_sensor_event: SensorEvent = None):
    """
    Updates an event in the database. If live event doesn't exist, initialize it.
    This assumes all events happen one after another, and cannot occur at the same time.

    Args:
        session (_type_): Session object. See module header.
        sensor_event (SensorEvent): Event that will be added to database
        event_type (int): -1 for default, 0 for heartbeat, 1 for data record, 2 for event summary
        prev_sensor_event (SensorEvent): Previous event to be used as a comparison and check for duplicates
    """
    logging.info("Attempting to update sensor event")

    # Query for an existing event with the same devEUI, live stream, and heartbeat CRC, with the highest ID
    existing_event: Event = session.scalars(
        select(Event).join(
            Event.sensor
        ).join(
            Event.deviceData
        ).filter(
            Event.isStreaming == True,
            Sensor.devEUI == sensor_event.devEUI,
            DeviceData.heartbeatRecordPayloadCRC == sensor_event.heartbeatRecordPayloadCRC,
        ).order_by(desc(Event.id))
    ).first()

    if existing_event is None:
        logging.info("No matching event found, creating a new one")
        sensor_event.isStreaming = True if eventType != 2 else False
        return add_sensor_event(session, sensor_event)

    # non-live events shouldn't be updated
    if existing_event.isStreaming == False:
        logging.warning("update_sensor_event(): Update of event failed. Attempted update of a non-live event")
        return

    # Transform sensor data to be compatible with db
    hidden_packets = sensor_event.hiddenDataIndices
    flattened_torque_data, record_numbers, record_lengths = flatten_data(sensor_event)

    # update list of packets to hide if event summary reached
    # if ((eventType == 2) and (prev_sensor_event != None)):
    #     hidden_packets = hide_duplicate_packets(flattened_torque_data, record_numbers, record_lengths, sensor_event.dataPacketPayloadCRCs,
    #                                             *flatten_data(prev_sensor_event), prev_sensor_event.calculatedDataPacketPayloadCRCs)

    # Set streaming to false if event summary reached
    if eventType == 2:
        existing_event.isStreaming = False

    # replace current event in db with sensor event. Sensor_event should be the updated version of the event
    logging.info("Found existing event, updating fields")

    existing_event.deviceData.lastTorqueBeforeSleep = sensor_event.lastTorqueBeforeSleep
    existing_event.deviceData.firstTorqueAfterSleep = sensor_event.firstTorqueAfterSleep
    existing_event.deviceData.recordNumbers = record_numbers
    existing_event.deviceData.recordLengths = record_lengths
    existing_event.deviceData.torqueData = flattened_torque_data
    existing_event.deviceData.hiddenDataIndices = hidden_packets
    existing_event.deviceData.typeOfStroke = sensor_event.typeOfStroke
    existing_event.deviceData.dataRecordPayloadCRCs = sensor_event.dataPacketPayloadCRCs
    existing_event.deviceData.calculatedDataRecordPayloadCRCs = sensor_event.calculatedDataPacketPayloadCRCs
    existing_event.deviceData.eventRecordPayloadCRC = sensor_event.eventSummaryPayloadCRC
    existing_event.deviceData.calculatedEventRecordPayloadCRC = sensor_event.calculatedEventSummaryPayloadCRC
    existing_event.deviceData.heartbeatRecordPayloadCRC = sensor_event.heartbeatRecordPayloadCRC
    existing_event.deviceData.calculatedHeartbeatRecordPayloadCRC = sensor_event.calculatedHeartbeatRecordPayloadCRC

    existing_event.deviceTrendInfo.strokeTime = sensor_event.strokeTime
    existing_event.deviceTrendInfo.maxTorque = sensor_event.maxTorque
    existing_event.deviceTrendInfo.temperature = sensor_event.temperature
    existing_event.deviceTrendInfo.batteryVoltage = sensor_event.batteryVoltage

    existing_event.deviceInfo.firmwareVersion = sensor_event.fwVersion
    existing_event.deviceInfo.pwaRevision = sensor_event.pwaVersion
    existing_event.deviceInfo.serialNumber = sensor_event.serialNumber
    existing_event.deviceInfo.deviceType = sensor_event.deviceType
    existing_event.deviceInfo.deviceLocation = sensor_event.deviceLocation
    existing_event.deviceInfo.diagnostic = sensor_event.diagnostic
    existing_event.deviceInfo.openValveCount = sensor_event.openValveCount
    existing_event.deviceInfo.closeValveCount = sensor_event.closeValveCount

def get_aux_sensors(session):
    return

def add_aux_sensor_data(session, aux_sensor_data: AuxSensorData):
    return

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
                           .filter_by(sensorID=sensor_id)
                           .options(joinedload(Event.deviceTrendInfo))
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
