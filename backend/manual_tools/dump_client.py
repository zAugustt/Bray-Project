# pragma: no cover

"""
Standalone python file meant for debugging purposes. This program dumps the message payloads from the MQTT broker into
files, requiring the `MQTT_USERNAME` and `MQTT_PASSWORD` to be set.

Example:
    `python dump_client.py`

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University

Date:
    November 2024
"""

import json, re
from typing import Any
from time import time
from os import getenv
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, ConnectFlags, MQTTMessage
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties
from paho.mqtt.enums import CallbackAPIVersion

# Data Dump Directory
DATA_DUMP_DIR = "data/"

# MQTT Configuration
MQTT_BROKER = '70.113.24.206'
MQTT_PORT = 1883
MQTT_TOPIC = [("sensors/+/port/+", 2)]
MQTT_USERNAME = getenv("MQTT_USERNAME")
MQTT_PASSWORD = getenv("MQTT_PASSWORD")

# Initialize MQTT Client
mqtt_client = Client(callback_api_version=CallbackAPIVersion.VERSION2)

# This will hold the messages received from MQTT
messages = []


def sanitize_topic(topic):
    # Replace `/` with `_`
    topic = topic.replace('/', '_')
    # Remove or replace non-filesystem characters
    topic = re.sub(r'[<>:"/\\|?*]', '_', topic)
    # Optionally truncate the string if needed
    return topic[:255]  # most systems allow up to 255 characters


def on_connect(client: Client, userdata: Any, flags: mqtt.ConnectFlags, reason_code: ReasonCode, 
               properties: Properties):
    print("Connected to MQTT broker with result code " + str(reason_code))
    client.subscribe(MQTT_TOPIC)  # Subscribe to the topic


def on_message(client: Client, userdata: Any, msg: MQTTMessage):
    payload: bytes = msg.payload
    topic: str = msg.topic

    print(f"Received from topic {topic} with payload: {payload}")
    messages.append(payload)  # Store received messages

    # Store msg in file
    with open(f"{DATA_DUMP_DIR}{time()}.{sanitize_topic(topic)}.data", "wb") as f:
        f.write(payload)
    print(f"Stored message with topic: {topic}")


# Connect to the MQTT broker
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


if __name__ == '__main__':
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()  # Start the MQTT client loop
