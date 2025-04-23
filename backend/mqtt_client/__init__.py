"""
MQTT Client Module

This module provides a `ThreadedMQTTClient` to capture and interpret messages sent to the MQTT broker.

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University   
    Aysen De La Cruz (delacruzaysen@gmail.com), Texas A&M University
    Alex Kearney (akearney2001@gmail.com), Texas A&M University
    Josh Werner (joshdwerner2@gmail.com), Texas A&M University


Date:
    November 2024
    March 2025
"""

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties
from paho.mqtt.enums import CallbackAPIVersion
from threading import Thread
from os import getenv
from typing import Dict, List, Any
from collections.abc import Callable
import logging
from typing import Union


from .sensor_event import SensorEvent
from .aux_sensor_event import AuxSensorEvent


class ThreadedMQTTClient(Thread):
    """
    Threaded (daemon) MQTT Client that interprets messages from topic into a `SensorEvent`.
    Executes callbacks when certain messages from certain topics are received. Topic should be in format of
    `sensors/<devEUI>/port/<portNumber>`.

    Raises:
        ValueError: When either username or password is not set.
    """
    mqtt_client: mqtt.Client = None
    dump_dir: str = "data"
    sensor_events: Dict[str, SensorEvent] = {}

    # Callbacks
    on_heartbeat_packet: Callable[[SensorEvent], None] = None
    on_data_packet: Callable[[SensorEvent], None] = None
    on_event_summary_packet: Callable[[SensorEvent], None] = None
    on_complete_event: Callable[[SensorEvent], None] = None
    on_co2_packet: Callable[[AuxSensorEvent], None] = None #callback for CO2 sensor

    # Broker Information
    broker: str = getenv("MQTT_HOST", "mosquitto")
    broker_port: int = 1883
    topics: str = [("sensors/+/port/+", 2)]
    #topics: List[tuple] = [("sensors/+/port/+", 2), ("sensors/co2", 2)] #include CO2 topic Note Published on same topic
    username: str = getenv("MQTT_USERNAME", None)
    password: str = getenv("MQTT_PASSWORD", None)

    def __init__(self, on_heartbeat_packet: Callable = None, on_data_packet: Callable = None, on_event_summary_packet: Callable = None, on_complete_event: Callable = None, 
                 on_co2_packet: Callable = None):
        """
        Initializes the object.

        Args:
            on_heartbeat_packet (Callable, optional): Executes when receiving a message from port 12. Defaults to None.
            on_data_packet (Callable, optional): Executes when receiving a message from port 13. Defaults to None.
            on_event_summary_packet (Callable, optional): Executes when receiving a message from port 14. Defaults to None.
            on_complete_event (Callable, optional): Deprecated.
        """
        super().__init__(daemon=True)  # Kill when parent process exits
        
        #Initialize MQTT client
        self.mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
        self.sensor_events = {}

        #Callbacks
        self.on_heartbeat_packet = on_heartbeat_packet
        self.on_data_packet = on_data_packet
        self.on_event_summary_packet = on_event_summary_packet
        self.on_complete_event = on_complete_event
        self.on_co2_packet = on_co2_packet

    def run(self):
        """
        Starts the threaded client.

        Raises:
            ValueError: When either username or password is not set.
        """
        logging.info(">> Starting threaded client.")

        # Verify if user/pass set
        if not self.username or not self.password:
            raise ValueError("Please set username and password env variables")

        # Add client callbacks and data
        self.mqtt_client.on_connect = ThreadedMQTTClient._on_connect
        self.mqtt_client.on_message = ThreadedMQTTClient._on_message
        self.mqtt_client.user_data_set({
            "topics": self.topics,
            "sensor_events": self.sensor_events,
            "on_heartbeat_packet": self.on_heartbeat_packet,
            "on_data_packet": self.on_data_packet,
            "on_event_summary_packet": self.on_event_summary_packet,
            "on_complete_event": self.on_complete_event,
            "on_co2_packet": self.on_co2_packet,
        })

        # Set auth, connect, subscribe
        try:
            self.mqtt_client.username_pw_set(self.username, self.password)
            err = self.mqtt_client.connect(self.broker, self.broker_port)
            logging.debug(f">> MQTTErrorCode: {err}")
            self.mqtt_client.subscribe(self.topics)
            logging.info(">> Subscribed and connected")
        except Exception as e:
            logging.error(f"Could not connect to MQTT broker {self.broker} with error: {e}")

        # Start CO2 sensor monitoring
        #if self.co2_sensor:
        #    Thread(target=self._monitor_co2, daemon=True).start()

        # Start polling (blocking)
        logging.info(f">> Looping forever!!!")
        self.mqtt_client.loop_forever()

    @staticmethod
    def _on_connect(client: mqtt.Client, userdata: Any, flags: mqtt.ConnectFlags, reason_code: ReasonCode,
                    properties: Properties):
        logging.info(f">> Connected to broker {client.host}:{client.port} with reason code: {reason_code}")

    @staticmethod
    def _on_subscribe(client: mqtt.Client, userdata: Any, mid: int, reason_code_list: List[ReasonCode],
                      properties: Properties):
        logging.info(f">> Subscription acknowledged with mid: {mid}")
        logging.debug(f">> Reason codes: {reason_code_list}")

    @staticmethod
    def _on_message(client: mqtt.Client, userdata: Any, msg: MQTTMessage):
        sensor_events: Dict[str, Dict[str, Union[SensorEvent, AuxSensorEvent]]] = userdata.get("sensor_events")
        on_heartbeat_packet: Callable | None = userdata.get("on_heartbeat_packet")
        on_data_packet: Callable | None = userdata.get("on_data_packet")
        on_event_summary_packet: Callable | None = userdata.get("on_event_summary_packet")
        on_co2_packet: Callable | None = userdata.get("on_co2_packet")

        payload: bytes = msg.payload
        topic: str = msg.topic

        _, devEUI, _, port, *_ = topic.strip().split("/")
        logging.info(f">> RECEIVED MESSAGE ON PORT {port}")

        # Add a new sensor event if it doesn't exist or get the existing one. Start with an empty current event
        if sensor_events.get(devEUI) is None:
            sensor_events[devEUI] = {
                "old_event": None,
                "current_event": AuxSensorEvent() if port == "15" else SensorEvent()
            }
        # Parse data for the current event
        event = sensor_events[devEUI]
        event["current_event"].parse_from_data(topic, payload)
        # Execute callbacks
        if port == "12":
            logging.info(">> Executing on_heartbeat_packet")
            event["current_event"] = AuxSensorEvent()
            on_heartbeat_packet(event["current_event"]) if on_heartbeat_packet is not None else None
            event["current_event"] = AuxSensorEvent()
        elif port == "13":
            logging.info(">> Executing on_data_packet")
            on_data_packet(event["current_event"]) if on_data_packet is not None else None
        elif port == "14":
            logging.info(">> Executing on_event_summary_packet")
            on_event_summary_packet(event["current_event"], event["old_event"]) if on_event_summary_packet is not None else None
            event["old_event"] = event["current_event"]
            del event["current_event"]
            event["current_event"] = AuxSensorEvent()
        elif port == "15":
            logging.info(">> Executing on_co2_packet")
            on_co2_packet(event["current_event"]) if on_co2_packet is not None else None
            del event["current_event"]
            event["current_event"] = SensorEvent()
