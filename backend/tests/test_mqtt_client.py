import pytest
from mqtt_client.sensor_event import SensorEvent
from mqtt_client.crc16 import CRC16_CCITT
from mqtt_client.misc import cstr_to_str
from mqtt_client.aux_sensor_event import AuxSensorEvent
from mqtt_client import ThreadedMQTTClient
from unittest.mock import MagicMock

class TestCRC:
    def test_crc_happy(self):
        data = [0x00, 0x0a, 0x00, 0x1b, 0x00, 0x2c, 0x00, 0x3d, 0x00, 0x4e]
        result = CRC16_CCITT(bytes(data))
        assert result == 1548

    def test_crc_short(self):
        data = b'\x01\x02\x03'
        result = CRC16_CCITT(data)
        assert isinstance(result, int)

class TestMisc:
    def test_cstr_str_happy(self):
        data = (b"\x68", b"\x65", b"\x6c", b"\x6c", b"\x6f", b"\x00")  # hello
        result = cstr_to_str(data)
        assert result == "hello"

    def test_cstr_str_rainy(self):
        data = (b"\x68", b"\x65", b"\x6c", b"\x6c", b"\x6f", b"\x00", b"\x77", b"\x6f", b"\x72", b"\x6c", b"\x64")  # hello (null byte) world
        result = cstr_to_str(data)
        assert result == "hello"

    def test_cstr_str_no_null(self):
        data = (b"\x68", b"\x65", b"\x6c")  # hel
        result = cstr_to_str(data)
        assert result == "hel"

class TestSensorEvent:
    def test_init(self):
        sensor_event = SensorEvent()
        assert sensor_event.torqueData == []
        assert sensor_event.dataPacketPayloadCRCs == []
        assert sensor_event.calculatedDataPacketPayloadCRCs == []

class TestAuxSensorEvent:
    def test_aux_sensor_event_parse_good(self):
        aux_event = AuxSensorEvent()
        topic = "sensor/ABC123/port/15"
        data = bytearray(b'\x00\x00\x00' + b'00010' + b'\x00\x00\x00' + bytes([2]) + b'\x00'*8)  # scaled CO₂ percentage
        aux_event.parse_from_data(topic, data)

        assert aux_event.devEUI == "ABC123"
        assert aux_event.co2_percentage == 20  # 10 * 2
        assert aux_event.timestamp is not None

    def test_aux_sensor_event_parse_short_data(self):
        aux_event = AuxSensorEvent()
        topic = "sensor/ABC123/port/15"
        data = b'\x00\x00\x00\x00'  # too short intentionally
        aux_event.parse_from_data(topic, data)  # Should not crash

    def test_aux_sensor_event_devEUI_mismatch(self):
        aux_event = AuxSensorEvent()
        topic = "sensor/ABC123/port/15"
        aux_event.parse_from_data(topic, b'\x00'*20)

        with pytest.raises(SyntaxError):
            aux_event.parse_from_data("sensor/DEF456/port/15", b'\x00'*20)

class TestThreadedMQTTClient:
    def test_threaded_client_init(self):
        client = ThreadedMQTTClient()
        assert client.broker == "mosquitto"
        assert client.broker_port == 1883
        assert client.dump_dir == "data"

    def test_threaded_client_run_fails_without_credentials(self):
        client = ThreadedMQTTClient()
        client.username = None
        client.password = None
        with pytest.raises(ValueError):
            client.run()

    def test_on_message_parse_heartbeat(self):
        fake_userdata = {
            "sensor_events": {},
            "on_heartbeat_packet": MagicMock(),
            "on_data_packet": None,
            "on_event_summary_packet": None,
            "on_co2_packet": None,
            "topics": []
        }
        fake_msg = MagicMock()
        fake_msg.payload = b"\x00" * 100
        fake_msg.topic = "sensor/ABC123/port/12"

        ThreadedMQTTClient._on_message(MagicMock(), fake_userdata, fake_msg)

        assert "ABC123" in fake_userdata["sensor_events"]

    def test_on_message_parse_co2(self):
        fake_userdata = {
            "sensor_events": {},
            "on_heartbeat_packet": None,
            "on_data_packet": None,
            "on_event_summary_packet": None,
            "on_co2_packet": MagicMock(),
            "topics": []
        }
        fake_msg = MagicMock()
        fake_msg.payload = b"\x00" * 100
        fake_msg.topic = "sensor/ABC123/port/15"

        ThreadedMQTTClient._on_message(MagicMock(), fake_userdata, fake_msg)

        assert "ABC123" in fake_userdata["sensor_events"]
