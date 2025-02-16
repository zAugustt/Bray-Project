"""
Module for transforming an `Event` into a CSV following the F2 format of CAMS software.

Authors:
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University
"""

from datetime import datetime
from db_connector import DBConnector
from db_connector import queries
from db_connector.models import Event


def format_event_data(event: Event, hide_packet_data: bool = False) -> dict:
    """
    Takes an event and process all fields, including omitting duplicate packets.

    Args:
        event (Event): object to process
        hide_packet_data (bool, optional): Omit duplicate packets. Defaults to False.

    Returns:
        dict: Dictionary containing event data
    """
    hide_packets = event.deviceData.hiddenDataIndices
    packet_numbers = event.deviceData.recordNumbers
    packet_lengths = event.deviceData.recordLengths
    data = event.deviceData.torqueData

    new_data = []
    new_packet_numbers = []
    new_packet_lengths = []
    index = 0

    # Hide data, record numbers, and lengths based on hidden packets
    if hide_packet_data:
        for i in range(len(packet_numbers)):
            packet_length = packet_lengths[i]
            if packet_numbers[i] not in hide_packets:
                new_data.extend(data[index:index + packet_length])
                new_packet_numbers.append(packet_numbers[i])
                new_packet_lengths.append(packet_length)
            index += packet_length
    else:
        new_data = data
        new_packet_numbers = packet_numbers
        new_packet_lengths = packet_lengths

    event_data = {
        "id": event.id,
        "timestamp": event.timestamp,
        "isStreaming": event.isStreaming,
        "firmwareVersion": event.deviceInfo.firmwareVersion,
        "pwaRevision": event.deviceInfo.pwaRevision,
        "serialNumber": event.deviceInfo.serialNumber,
        "deviceType": event.deviceInfo.deviceType,
        "deviceLocation": event.deviceInfo.deviceLocation,
        "diagnostic": event.deviceInfo.diagnostic,
        "openValveCount": event.deviceInfo.openValveCount,
        "closeValveCount": event.deviceInfo.closeValveCount,
        "strokeTime": event.deviceTrendInfo.strokeTime,
        "maxTorque": event.deviceTrendInfo.maxTorque,
        "hiddenDataIndices": hide_packets,
        "temperature": event.deviceTrendInfo.temperature,
        "batteryVoltage": event.deviceTrendInfo.batteryVoltage,
        "lastTorqueBeforeSleep": event.deviceData.lastTorqueBeforeSleep,
        "firstTorqueAfterSleep": event.deviceData.firstTorqueAfterSleep,
        "recordNumbers": new_packet_numbers,
        "recordLengths": new_packet_lengths,
        "torqueData": new_data,
        "typeOfStroke": event.deviceData.typeOfStroke,
        "dataRecordPayloadCRCs": event.deviceData.dataRecordPayloadCRCs,
        "calculatedDataRecordPayloadCRCs": event.deviceData.calculatedDataRecordPayloadCRCs,
        "eventRecordPayloadCRC": event.deviceData.eventRecordPayloadCRC,
        "calculatedEventRecordPayloadCRC": event.deviceData.calculatedEventRecordPayloadCRC,
        "heartbeatRecordPayloadCRC": event.deviceData.heartbeatRecordPayloadCRC,
        "calculatedHeartbeatRecordPayloadCRC": event.deviceData.calculatedHeartbeatRecordPayloadCRC,
    }
    return event_data


def fetch_event_data(conn: DBConnector, sensor_id: int, event_id: int) -> dict:
    """
    Fetches event data from the database.

    Args:
        conn (DBConnector): Database connector
        sensor_id (int): Sensor id
        event_id (int): Event id

    Returns:
        dict: Dictionary containing event data
    """
    # Fetch the event data from the database
    event = conn.execute_query_readonly(queries.get_event, sensor_id, event_id)

    # Extract and structure the event data
    event_data = {
        "id": event.id,
        "isStreaming": event.isStreaming,
        "timestamp": event.timestamp,
        "firmwareVersion": event.deviceInfo.firmwareVersion,
        "pwaRevision": event.deviceInfo.pwaRevision,
        "serialNumber": event.deviceInfo.serialNumber,
        "deviceType": event.deviceInfo.deviceType,
        "deviceLocation": event.deviceInfo.deviceLocation,
        "diagnostic": event.deviceInfo.diagnostic,
        "openValveCount": event.deviceInfo.openValveCount,
        "closeValveCount": event.deviceInfo.closeValveCount,
        "strokeTime": event.deviceTrendInfo.strokeTime,
        "maxTorque": event.deviceTrendInfo.maxTorque,
        "temperature": event.deviceTrendInfo.temperature,
        "batteryVoltage": event.deviceTrendInfo.batteryVoltage,
        "lastTorqueBeforeSleep": event.deviceData.lastTorqueBeforeSleep,
        "firstTorqueAfterSleep": event.deviceData.firstTorqueAfterSleep,
        "recordNumbers": event.deviceData.recordNumbers,
        "recordLengths": event.deviceData.recordLengths,
        "torqueData": event.deviceData.torqueData,
        "hiddenDataIndices": event.deviceData.hiddenDataIndices,
        "typeOfStroke": event.deviceData.typeOfStroke,
        "dataRecordPayloadCRCs": event.deviceData.dataRecordPayloadCRCs,
        "calculatedDataRecordPayloadCRCs": event.deviceData.calculatedDataRecordPayloadCRCs,
        "eventRecordPayloadCRC": event.deviceData.eventRecordPayloadCRC,
        "calculatedEventRecordPayloadCRC": event.deviceData.calculatedEventRecordPayloadCRC,
        "heartbeatRecordPayloadCRC": event.deviceData.heartbeatRecordPayloadCRC,
        "calculatedHeartbeatRecordPayloadCRC": event.deviceData.calculatedHeartbeatRecordPayloadCRC,
    }
    return event_data


def write_event_csv(csv_writer, event_data: dict, hidden_data: bool = False):
    """
    Writes event data to a csv.

    Args:
        csv_writer (_csv._writer): Object from `csv.writer()`
        event_data (dict): Dictionary containing event data
        hidden_data (bool, optional): Omit duplicate packets. Defaults to False.
    """
    # Writing the required format to the CSV file
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow([f"File Created: {current_timestamp}"])
    csv_writer.writerow([f"{'Warning! Event not completed!' if event_data['isStreaming'] else ''}"])

    csv_writer.writerow(["Firmware"])
    csv_writer.writerow([f"File Format Rev: {event_data['firmwareVersion']}"])
    csv_writer.writerow([])
    csv_writer.writerow([f"Device SN: {event_data['serialNumber']}"])
    csv_writer.writerow([f"Device Type: {event_data['deviceType']}"])
    csv_writer.writerow([f"Device Location: {event_data['deviceLocation']}"])
    csv_writer.writerow([])

    csv_writer.writerow(["Heartbeat Record"])
    csv_writer.writerow(["================"])
    csv_writer.writerow([f"Battery (mv): {event_data['batteryVoltage']}"])
    csv_writer.writerow([f"Temperature (C): {event_data['temperature']}"])
    csv_writer.writerow([f"Diagnostic: {event_data['diagnostic']}"])
    csv_writer.writerow([f"Valve Open Count: {event_data['openValveCount']}"])
    csv_writer.writerow([f"Valve Close Count: {event_data['closeValveCount']}"])
    csv_writer.writerow([f"Last Torque Before Sleep (uv): {event_data['lastTorqueBeforeSleep']}"])
    csv_writer.writerow([f"First Torque After Sleep (uv): {event_data['firstTorqueAfterSleep']}"])
    csv_writer.writerow([])

    csv_writer.writerow(["Event Summary Record"])
    csv_writer.writerow(["===================="])
    csv_writer.writerow([f"Type of Stroke: {'Open' if (event_data['typeOfStroke'] == 1) else ('Close' if event_data['typeOfStroke'] == 2 else 'N/A')}"])
    csv_writer.writerow([f"Stroke Time (ms): {event_data['strokeTime']}"])
    csv_writer.writerow([f"Peak Torque (uv): {event_data['maxTorque']}"])
    csv_writer.writerow([])
    csv_writer.writerow(["Rec", "Torque", "CRC", "CALC_CRC", "P/F"])

    torque_index = 0
    for record_number, record_length in zip(event_data['recordNumbers'], event_data['recordLengths']):
        # If hidden data is specified, skip hidden packets
        if hidden_data and record_number in event_data['hiddenDataIndices']:
            continue

        data_crc = event_data['dataRecordPayloadCRCs'][record_number - 1] if (record_number - 1) < len(event_data['dataRecordPayloadCRCs']) else ""
        calculated_crc = event_data['calculatedDataRecordPayloadCRCs'][record_number - 1] if (record_number - 1) < len(event_data['calculatedDataRecordPayloadCRCs']) else " "
        status = 'P' if (data_crc == calculated_crc) else 'F'

        csv_writer.writerow([
            record_number,  # Only write record number for the first row in each packet
            event_data['torqueData'][torque_index],
            data_crc,
            calculated_crc,
            status
        ])
        torque_index += 1

        # Rest of rows (not first) don't print the record number
        for _ in range(1, record_length):
            csv_writer.writerow(["", event_data['torqueData'][torque_index]])
            torque_index += 1
