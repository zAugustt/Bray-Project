import pytest
import os
from os.path import join
from flask import Flask
from api_v1 import api_v1

SAMPLE_DATA="tests/sample_data"  # Bray TAMU capstone firmware


def create_app():
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
    })
    app.register_blueprint(api_v1, url_prefix="/api_v1")
    return app


@pytest.fixture
def client():
    # Create and configure a new app instance for each test
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def event_heartbeat_packet_payload():
    filepath = join(SAMPLE_DATA, "original/1729792596.4154148.sensors_39-32-30-31-79-30-6f-02_port_12.data")
    _, _, name, _ = filepath.split(".")
    topic = "/".join(name.split("_"))
    yield topic, open(filepath, "rb").read()


@pytest.fixture
def event_data_packet_payloads():
    folderpath = join(SAMPLE_DATA, "original")
    topic_payloads = []

    for filename in os.listdir(folderpath):
        filepath = os.path.join(folderpath, filename)
        if not os.path.isfile(filepath):
            continue
        _, _, name, _ = filename.split(".")
        topic = "/".join(name.split("_"))
        port = name.split("_")[-1]

        if port == "13":
            topic_payloads.append((topic, open(filepath, "rb").read()))
    
    yield topic_payloads


@pytest.fixture
def event_summary_packet_payload():
    filepath = join(SAMPLE_DATA, "original/1729792706.9500625.sensors_39-32-30-31-79-30-6f-02_port_14.data")
    _, _, name, _ = filepath.split(".")
    topic = "/".join(name.split("_"))
    yield topic, open(filepath, "rb").read()


@pytest.fixture
def sensor_event_data(event_heartbeat_packet_payload, event_data_packet_payloads, event_summary_packet_payload):
    topic_payloads = [
        (f"{event_heartbeat_packet_payload[0]}", event_heartbeat_packet_payload[1]),
        *[(f"{packet[0]}", packet[1]) for packet in event_data_packet_payloads],
        (f"{event_summary_packet_payload[0]}", event_summary_packet_payload[1]),
    ]
    yield topic_payloads
