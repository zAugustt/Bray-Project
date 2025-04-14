"""
SensorEvent Module

This module provides a `SensorEvent` which parses byte data into python objects. See
[this repository](<https://github.com/Trans-Opt/Bray-LoRa-Firmware>) for detailed packet breakdown.

NOTE: The `SMART DEVICE COMM` document and firmware do not follow the same structure for battery
voltage and temperature. The packet parser follows the firmware's implementation.

NOTE: The `SMART DEVICE COMM` document and firmware do not agree on a value for `typeOfStroke`. The
documentation has the values of 0 and 1, while the firmware has values of 0 (undefined), 1 (open), and 2 (closed).

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University

Date:
    November 2024
"""

import logging
from typing import List
from struct import unpack   # See https://docs.python.org/3.11/library/struct.html#format-characters
from .misc import cstr_to_str
from .crc16 import CRC16_CCITT


class SensorEvent:
    """
    Data structure holding information on a sensor event. See the Smart Dev Comm documentation and `app.h` in firmware
    for packet structure breakdowns.
    """
    devEUI: str = None

    # Event Summary Record
    typeOfStroke: int = 0
    strokeTime: int = 0
    maxTorque: int = 0
    eventSummaryPayloadCRC: int = 0
    calculatedEventSummaryPayloadCRC: int = 0

    # Data record
    torqueData: List[List[int]]
    dataPacketPayloadCRCs: List[int]
    calculatedDataPacketPayloadCRCs: List[int]
    hiddenDataIndices: List[int]

    # Heartbeat record
    fwVersion: int = 0
    pwaVersion: int = 0
    serialNumber: int = 0
    deviceType: int = 0
    deviceLocation: int = 0
    deviceInfoCRC: int = 0
    month: int = 1
    day: int = 1
    year: int = 1
    hour: int = 0
    minute: int = 0
    second: int = 0
    batteryVoltage: int = 0
    temperature: int = 0
    diagnostic: int = 0
    openValveCount: int = 0
    closeValveCount: int = 0
    lastTorqueBeforeSleep: int = 0
    firstTorqueAfterSleep: int = 0
    dataUnits: int = 0              # Not transferred
    calibrationFactor: int = 0      # Not transferred
    heartbeatRecordPayloadCRC: int = 0
    calculatedHeartbeatRecordPayloadCRC: int = 0

    # Stream
    isStreaming: bool = False

    def __init__(self):
        self.torqueData = []
        self.dataPacketPayloadCRCs = []
        self.calculatedDataPacketPayloadCRCs = []
        self.hiddenDataIndices = []

    def parse_from_data(self, topic: str, data: bytes) -> None:
        """
        Attempts to interpret the data from a series of bytes.

        Args:
            topic (str): MQTT topic. Should follow the format `sensor/<devEUI>/port/<port>`.
            data (bytes): Data to be read.

        Raises:
            SyntaxError: Raised after loading data that has a different `devEUI` than previously read data.
            SyntaxError: Raised after reading data from an unrecognized port number (valid ports are 12, 13, 14).
        """
        # Parse devEUI and port from topic
        _, devEUI, _, port = topic.strip().split("/")

        # Ensure data being read matches the sensor
        if self.devEUI is None:
            self.devEUI = devEUI
            logging.debug(f"Found devEUI: {self.devEUI}")
        elif self.devEUI != devEUI:
            raise SyntaxError("DevEUI mismatch!")

        # Parse data
        match port:
            case "12":
                self.parse_from_heartbeat_record(data)
            case "13":
                self.parse_from_data_record(data)
            case "14":
                self.parse_from_event_summary_record(data)
            case _:
                raise SyntaxError(f"Unrecognized packet from port {port}")

    def parse_from_event_summary_record(self, data: bytes) -> None:
        """
        Interprets byte data as an event summary record.

        Args:
            data (bytes): Data to be interpreted.
        """
        logging.debug("Loading event summary record...")
        self.typeOfStroke = unpack("<H", data[:2])[0]
        self.strokeTime = unpack("<H", data[2:4])[0]
        self.maxTorque = unpack("<h", data[4:6])[0]
        self.eventSummaryPayloadCRC = unpack("<H", data[20:22])[0]
        self.calculatedEventSummaryPayloadCRC = CRC16_CCITT(data[:-2])

        if self.eventSummaryPayloadCRC != self.calculatedEventSummaryPayloadCRC:
            logging.warning(f"Event summary record CRCs do not match. Actual: {self.eventSummaryPayloadCRC} Calculated: {self.calculatedEventSummaryPayloadCRC}")

    def parse_from_data_record(self, data: bytes) -> None:
        """
        Interprets byte data as a data record.

        Args:
            data (bytes): Data to be interpreted.
        """
        logging.debug("Loading data record...")
        packet_seq: int = unpack("<H", data[:2])[0]
        packet_torque_data: List[int] = []

        # Increase torque data list to proper length
        len_diff: int = packet_seq - len(self.torqueData)
        if len_diff > 0:
            self.torqueData.extend([None] * len_diff)
            self.dataPacketPayloadCRCs.extend([None] * len_diff)
            self.calculatedDataPacketPayloadCRCs.extend([None] * len_diff)

        if self.torqueData[packet_seq - 1] is not None:
            logging.warning(f"Overwriting existing packet data for packet {packet_seq}!")

        for i in range(2, len(data[2:-1]), 2):
            packet_torque_data.append(unpack("<h", data[i:i + 2])[0])

        # Interpret CRC
        dataPacketPayloadCRC = unpack("<H", data[-2:])[0]
        calculatedDataPacketPayloadCRC = CRC16_CCITT(data[:-2])

        if dataPacketPayloadCRC != calculatedDataPacketPayloadCRC:
            logging.warning(f"Data record CRCs do not match. Actual: {dataPacketPayloadCRC} Calculated {calculatedDataPacketPayloadCRC}")

        self.torqueData[packet_seq - 1] = packet_torque_data
        self.dataPacketPayloadCRCs[packet_seq - 1] = dataPacketPayloadCRC
        self.calculatedDataPacketPayloadCRCs[packet_seq - 1] = calculatedDataPacketPayloadCRC

    def parse_from_heartbeat_record(self, data: bytes) -> None:
        """
        Interprets byte data as a heartbeat record.

        Args:
            data (bytes): Data to be interpreted.
        """
        logging.debug("Loading heartbeat record...")
        self.fwVersion = cstr_to_str(unpack("<cccc", data[:4]))
        self.pwaVersion = cstr_to_str(unpack("<cc", data[4:6]))
        self.serialNumber = cstr_to_str(unpack("<" + 'c' * 16, data[6:22]))
        self.deviceType = cstr_to_str(unpack("<" + 'c' * 16, data[22:38]))
        self.deviceLocation = cstr_to_str(unpack("<" + 'c' * 26, data[38:64]))
        self.deviceInfoCRC = unpack("<H", data[64:66])[0]  # Never calculated in firmware
        self.month = unpack("<B", data[66:67])[0]
        self.day = unpack("<B", data[67:68])[0]
        self.year = unpack("<B", data[68:69])[0] + 2000
        self.hour = unpack("<B", data[69:70])[0]
        self.minute = unpack("<B", data[70:71])[0]
        self.second = unpack("<B", data[71:72])[0]
        self.temperature = unpack("<h", data[72:74])[0]     # NOTE: THESE ARE SWITCHED AROUND IN THE DOCS AND FIRMWARE
        self.batteryVoltage = unpack("<H", data[74:76])[0]  # NOTE: THESE ARE SWITCHED AROUND IN THE DOCS AND FIRMWARE
        self.diagnostic = unpack("<B", data[76:77])[0]
        self.openValveCount = unpack("<H", data[77:79])[0]
        self.closeValveCount = unpack("<H", data[79:81])[0]
        self.lastTorqueBeforeSleep = unpack("<h", data[81:83])[0]
        self.firstTorqueAfterSleep = unpack("<h", data[83:85])[0]
        self.dataUnits = unpack("<B", data[85:86])[0]               # Not transferred
        self.calibrationFactor = unpack("<B", data[86:87])[0]       # Not transferred
        self.heartbeatRecordPayloadCRC = unpack("<H", data[94:96])[0]

        # Calculate CRCs
        self.calculatedHeartbeatRecordPayloadCRC = CRC16_CCITT(data[:-2])
        if self.calculatedHeartbeatRecordPayloadCRC != self.heartbeatRecordPayloadCRC:
            logging.warning(f"Heartbeat record CRCs do not match. Actual: {self.heartbeatRecordPayloadCRC} Calculated: {self.calculatedHeartbeatRecordPayloadCRC}")
            

    def __repr__(self) -> str:
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)
