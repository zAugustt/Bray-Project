from mqtt_client.sensor_event import SensorEvent
from mqtt_client.crc16 import CRC16_CCITT
from mqtt_client.misc import cstr_to_str


class TestCRC:
    def test_crc_happy(self):
        data = [0x00, 0x0a, 0x00, 0x1b, 0x00, 0x2c, 0x00, 0x3d, 0x00, 0x4e]
        result = CRC16_CCITT(bytes(data))

        assert result == 1548


class TestMisc:
    def test_cstr_str_happy(self):
        data = (b"\x68", b"\x65", b"\x6c", b"\x6c", b"\x6f", b"\x00")  # hello
        result = cstr_to_str(data)

        assert result == "hello"
    
    def test_cstr_str_rainy(self):
        data = (b"\x68", b"\x65", b"\x6c", b"\x6c", b"\x6f", b"\x00", b"\x77", b"\x6f", b"\x72", b"\x6c", b"\x64")  # hello (null byte) world
        result = cstr_to_str(data)

        assert result == "hello"


class TestSensorEvent:
    def test_init(self):
        sensor_event = SensorEvent()

        assert sensor_event.torqueData is not None
        assert sensor_event.dataPacketPayloadCRCs is not None
        assert sensor_event.calculatedDataPacketPayloadCRCs is not None
        assert len(sensor_event.torqueData) == 0
        assert len(sensor_event.dataPacketPayloadCRCs) == 0
        assert len(sensor_event.calculatedDataPacketPayloadCRCs) == 0
    
    def test_parse_event_summary_record(self, event_summary_packet_payload):
        _, data_bytes = event_summary_packet_payload
        sensor_event = SensorEvent()

        sensor_event.parse_from_event_summary_record(data_bytes)

        assert sensor_event.typeOfStroke == 1
        assert sensor_event.strokeTime == 12224  # This may be calculated inaccurately
        assert sensor_event.maxTorque == 65448  # This may be calculated inaccurately
        assert sensor_event.eventSummaryPayloadCRC == 4711
        assert sensor_event.calculatedEventSummaryPayloadCRC == 4711

    def test_parse_data_record(self, event_data_packet_payloads):
        sensor_event = SensorEvent()

        for _, data_bytes in event_data_packet_payloads:
            sensor_event.parse_from_data_record(data_bytes)
        
        actual_torque_data = [[9, 8, 6, 5, 4, 3, 2, 0, 0, 0, -1, -2, -3, -3, -4, -5, -7, -12, -19, -23, -28, -34, -42, -48, -54, -60, -65, -69, -74, -79, -82, -85, -87, -88, -88, -83, -77, -74, -72, -70, -69, -67, -66, -64, -63, -63, -62, -60, -58, -57],
                              [-54, -52, -51, -49, -48, -49, -49, -49, -48, -47, -47, -48, -48, -48, -50, -51, -51, -52, -53, -54, -55, -57, -58, -60, -61, -63, -65, -67, -68, -68, -51, -34, -33, -33, -32, -32, -31, -32, -32, -31, -31, -31, -31, -31, -31, -30, -30, -30, -30, -30],
                              [-29, -30, -29, -29, -29, -29, -29, -29, -29, -29, -29, -28, -28, -28, -28, -28, -28, -28, -28, -28, -28, -28, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -26, -26, -27, -27, -27, -27, -27, -27, -27, -27, -26, -26, -27, -27, -27],
                              [-27, -26, -27, -27, -27, -26, -26, -26, -26, -26, -26, -26, -26, -26, -25, -25, -25, -26, -25, -25, -26, -25, -25, -25, -25, -25, -25, -25, -25, -26, -25, -25, -25, -24, -25, -25, -25, -24, -24, -25, -25, -25, -25, -25, -25, -25, -25, -25, -25, -25],
                              [-25, -24, -24, -24, -25, -25, -25, -25, -25, -25, -25, -25, -24, -25, -25, -25, -25, -24, -24, -24, -25, -25, -24, -24, -24, -24, -24, -24, -24, -25, -25, -24, -24, -24, -25, -24, -24, -24, -24, -24, -24, -23, -24, -24, -24, -24, -24, -23, -24, -23],
                              [-23, -24, -25, -24, -24, -24, -24, -24, -24, -24, -23, -24, -24, -24, -24, -23, -24, -24, -24, -24, -23, -23, -23, -23, -23, -23, -24, -23, -24, -24, -24, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23],
                              [-24, -24, -24, -24, -23, -23, -24, -23, -24, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -22],
                              [-23, -23, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -22, -23, -22, -22, -23, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -23, -23, -23, -23, -23, -23],
                              [-23, -23, -22, -22, -23, -23, -23, -23, -23, -23, -22, -22, -22, -23, -23, -22, -22, -22, -23, -22, -22, -23, -23, -22, -22, -23, -23, -22, -23, -22, -22, -23, -23, -23, -23, -23, -22, -22, -23, -23, -23, -22, -23, -24, -23, -22, -22, -22, -23, -23],
                              [-23, -22, -22, -22, -22, -23, -23, -22, -22, -23, -23, -22, -22, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -22, -22, -22, -22, -23, -23, -22, -22, -22, -22, -22, -22, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -22]]
        assert sensor_event.torqueData == actual_torque_data
        assert sensor_event.dataPacketPayloadCRCs == [11782, 17957, 24275, 31461, 2156, 7408, 65346, 25669, 52067, 38300]
        assert sensor_event.calculatedDataPacketPayloadCRCs == [11782, 17957, 24275, 31461, 2156, 7408, 65346, 25669, 52067, 38300]

# TODO :: test instance where CRC does not match

    def test_parse_heartbeat_record(self, event_heartbeat_packet_payload):
        _, data_bytes = event_heartbeat_packet_payload
        sensor_event = SensorEvent()

        sensor_event.parse_from_heartbeat_record(data_bytes)

        assert sensor_event.fwVersion == "3.2"
        assert sensor_event.pwaVersion == "C"
        assert sensor_event.serialNumber == "IOT-0092R2"
        assert sensor_event.deviceType == "S92-RES 2\" BV"
        assert sensor_event.deviceLocation == "Bray RnD Lab"
        assert sensor_event.deviceInfoCRC == 0
        assert sensor_event.month == 1
        assert sensor_event.day == 1
        assert sensor_event.year == 2000
        assert sensor_event.hour == 0
        assert sensor_event.minute == 4
        assert sensor_event.second == 17
        assert sensor_event.temperature == 24
        assert sensor_event.batteryVoltage == 3031
        assert sensor_event.diagnostic == 32
        assert sensor_event.openValveCount == 22965
        assert sensor_event.closeValveCount == 29440
        assert sensor_event.lastTorqueBeforeSleep == 24
        assert sensor_event.firstTorqueAfterSleep == 28
        # dataUnits not tested bc firmware does not transfer
        # calibrationFactor not tested bc firmware does not transfer
        assert sensor_event.heartbeatRecordPayloadCRC == 14913
        assert sensor_event.calculatedHeartbeatRecordPayloadCRC == 14913

    def test_parse_data(self, sensor_event_data):
        sensor_event = SensorEvent()

        for topic, message in sensor_event_data:
            sensor_event.parse_from_data(topic, message)
        
        assert sensor_event.devEUI == "39-32-30-31-79-30-6f-02"
        assert sensor_event.fwVersion == "3.2"
        assert sensor_event.pwaVersion == "C"
        assert sensor_event.serialNumber == "IOT-0092R2"
        assert sensor_event.deviceType == "S92-RES 2\" BV"
        assert sensor_event.deviceLocation == "Bray RnD Lab"
        assert sensor_event.deviceInfoCRC == 0
        assert sensor_event.month == 1
        assert sensor_event.day == 1
        assert sensor_event.year == 2000
        assert sensor_event.hour == 0
        assert sensor_event.minute == 4
        assert sensor_event.second == 17
        assert sensor_event.temperature == 24
        assert sensor_event.batteryVoltage == 3031
        assert sensor_event.diagnostic == 32
        assert sensor_event.openValveCount == 22965
        assert sensor_event.closeValveCount == 29440
        assert sensor_event.lastTorqueBeforeSleep == 24
        assert sensor_event.firstTorqueAfterSleep == 28 
        assert sensor_event.heartbeatRecordPayloadCRC == 14913
        assert sensor_event.calculatedHeartbeatRecordPayloadCRC == 14913
        actual_torque_data = [[9, 8, 6, 5, 4, 3, 2, 0, 0, 0, -1, -2, -3, -3, -4, -5, -7, -12, -19, -23, -28, -34, -42, -48, -54, -60, -65, -69, -74, -79, -82, -85, -87, -88, -88, -83, -77, -74, -72, -70, -69, -67, -66, -64, -63, -63, -62, -60, -58, -57],
                              [-54, -52, -51, -49, -48, -49, -49, -49, -48, -47, -47, -48, -48, -48, -50, -51, -51, -52, -53, -54, -55, -57, -58, -60, -61, -63, -65, -67, -68, -68, -51, -34, -33, -33, -32, -32, -31, -32, -32, -31, -31, -31, -31, -31, -31, -30, -30, -30, -30, -30],
                              [-29, -30, -29, -29, -29, -29, -29, -29, -29, -29, -29, -28, -28, -28, -28, -28, -28, -28, -28, -28, -28, -28, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -26, -26, -27, -27, -27, -27, -27, -27, -27, -27, -26, -26, -27, -27, -27],
                              [-27, -26, -27, -27, -27, -26, -26, -26, -26, -26, -26, -26, -26, -26, -25, -25, -25, -26, -25, -25, -26, -25, -25, -25, -25, -25, -25, -25, -25, -26, -25, -25, -25, -24, -25, -25, -25, -24, -24, -25, -25, -25, -25, -25, -25, -25, -25, -25, -25, -25],
                              [-25, -24, -24, -24, -25, -25, -25, -25, -25, -25, -25, -25, -24, -25, -25, -25, -25, -24, -24, -24, -25, -25, -24, -24, -24, -24, -24, -24, -24, -25, -25, -24, -24, -24, -25, -24, -24, -24, -24, -24, -24, -23, -24, -24, -24, -24, -24, -23, -24, -23],
                              [-23, -24, -25, -24, -24, -24, -24, -24, -24, -24, -23, -24, -24, -24, -24, -23, -24, -24, -24, -24, -23, -23, -23, -23, -23, -23, -24, -23, -24, -24, -24, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23],
                              [-24, -24, -24, -24, -23, -23, -24, -23, -24, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -22],
                              [-23, -23, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -23, -23, -24, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -22, -23, -22, -22, -23, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -23, -23, -23, -23, -23, -23],
                              [-23, -23, -22, -22, -23, -23, -23, -23, -23, -23, -22, -22, -22, -23, -23, -22, -22, -22, -23, -22, -22, -23, -23, -22, -22, -23, -23, -22, -23, -22, -22, -23, -23, -23, -23, -23, -22, -22, -23, -23, -23, -22, -23, -24, -23, -22, -22, -22, -23, -23],
                              [-23, -22, -22, -22, -22, -23, -23, -22, -22, -23, -23, -22, -22, -23, -23, -23, -23, -23, -23, -22, -23, -23, -22, -22, -22, -22, -22, -23, -23, -22, -22, -22, -22, -22, -22, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -23, -22]]
        assert sensor_event.torqueData == actual_torque_data
        assert sensor_event.dataPacketPayloadCRCs == [11782, 17957, 24275, 31461, 2156, 7408, 65346, 25669, 52067, 38300]
        assert sensor_event.calculatedDataPacketPayloadCRCs == [11782, 17957, 24275, 31461, 2156, 7408, 65346, 25669, 52067, 38300]
        assert sensor_event.typeOfStroke == 1
        assert sensor_event.strokeTime == 12224  # This may be calculated inaccurately
        assert sensor_event.maxTorque == 65448  # This may be calculated inaccurately
        assert sensor_event.eventSummaryPayloadCRC == 4711
        assert sensor_event.calculatedEventSummaryPayloadCRC == 4711
