"""
SensorEvent Module

This module provides a `AuxSensorEvent` which parses byte data into python objects. See
[this repository](<https://github.com/Trans-Opt/Bray-LoRa-Firmware>) for detailed packet breakdown.

Authors:
    Aysen De La Cruz (delacruzaysen@gmail.com), Texas A&M University
    Josh Werner (joshdwerner2@gmail.com), Texas A&M University

Date:
    November 2024
"""

import logging
from typing import List
from struct import unpack   # See https://docs.python.org/3.11/library/struct.html#format-characters
from .misc import cstr_to_str
from .crc16 import CRC16_CCITT
from datetime import datetime


class AuxSensorEvent:
    """
    Data structure holding information on a sensor event. See the Smart Dev Comm documentation and `app.h` in firmware
    for packet structure breakdowns.
    """
    devEUI: str = None
    
    #CO2 sensor field
    co2_percentage: int = None 
    #hardcoding the aux sensor data
    aux_sensor_id: int = 6

    def __init__(self):
        self.timestamp = None

    def parse_from_data(self, topic: str, data: bytes) -> None:
        """
        Attempts to interpret the data from a series of bytes.

        Args:
            topic (str): MQTT topic. Should follow the format `sensor/<devEUI>/port/<port>`.
            data (bytes): Data to be read.

        Raises:
            SyntaxError: Raised after loading data that has a different `devEUI` than previously read data.
            SyntaxError: Raised after reading data from an unrecognized port number (valid ports are only 15).
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
            case "15":
                self.parse_from_co2_record(data)
            case _:
                raise SyntaxError(f"Unrecognized packet from port {port}")

    
    def parse_from_co2_record(self, data: bytes) -> None:
        """
        Interprets byte data as a CO2 record.
        TODO: Adjust according to data packet length 
        Args:
            data (bytes): Payload containing CO2 concentration (ppm)
        """
        logging.debug("Loading CO2 record...")
        if len(data) < 20:
            logging.warning("CO2 packet too short")
            return
        
        base_str = data[3:8].decode("utf-8") 
        base_value = int(base_str)

        scaling_factor = data[12]
        self.co2_percentage = base_value * scaling_factor
        #self.co2_percentage =  data[3:8].decode("utf-8")
        #self.co2_percentage = self.co2_percentage * int(data[12])
            
        logging.info(f"Data as bytes: {data.hex()}")
        self.timestamp = datetime.now()
        logging.info(f"CO2 parsed (XX.XXX %): {self.co2_percentage} % ")
        

    def __repr__(self) -> str:
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)
