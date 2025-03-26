"""
API v1

This module provides a blueprint containing Flask endpoints to handle HTTP requests. The default prefix for this
blueprint is found in `app.py`. For example, if the prefix is `api_v1`, then a complete route would look like
`/api_v1/sensors`.

This module also runs the `ThreadedMQTTClient`, which updates the database based on the messages
sent to the MQTT broker.

Endpoints:
    /sensors (GET): List of sensors
    /sensors/<int:sensor_id>/events (GET): List of events for given sensor ID with trend information
    /sensors/<int:sensor_id>/events/last/<int:last_n_events> (GET): List of events for given sensor ID with trend
                                                                    information for last n_events.
    /sensors/<int:sensor_id>/events/<int:event_id> (GET): Event information for given event ID without hidden data
    /sensors/<int:sensor_id>/events/<int:event_id>/hidden (GET): Event information for given event ID with hidden data
    /sensors/<int:sensor_id>/events/<int:event_id>/download (GET): Event CSV for given event ID without hidden data
    /sensors/<int:sensor_id>/events/<int:event_id>/download/hidden (GET): Event CSV for given event ID with hidden data

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University

Date:
    November-19-2024
"""


from flask import Blueprint, jsonify, Response, request
from db_connector import DBConnector, queries
from mqtt_client import ThreadedMQTTClient
from mqtt_client.sensor_event import SensorEvent
import logging, csv
from io import StringIO
from .custom_csv import fetch_event_data, format_event_data, write_event_csv


api_v1 = Blueprint("api_v1", __name__)

# Create database connection
_conn = DBConnector()


@api_v1.route("/sensors")
def sensors():
    """
    Returns a JSON object containing a list of sensors. Also provides devEUI and number of events associated with
    sensor.
    """
    sensors = _conn.execute_query_readonly(queries.get_sensors)
    sensor_datas = [{"id": sensor.id, "devEUI": sensor.devEUI, "numEvents": len(sensor.events)} for sensor in sensors]
    return jsonify(sensor_datas)


@api_v1.route("/sensors/<int:sensor_id>/events")
@api_v1.route("/sensors/<int:sensor_id>/events/last/<int:last_n_events>")  # Convert to POST endpoint if more options needed
def events(sensor_id: int, last_n_events: int = 30):
    """
    Returns a JSON object containing a list of events, as well as trend data for the last n events.

    Args:
        sensor_id (int): ID of sensor.
        last_n_events (int, optional): Number of events to use for trend info. Defaults to 30.
    """
    # Get event data
    events = _conn.execute_query_readonly(queries.get_events, sensor_id)
    event_datas = [{"id": event.id, "timestamp": event.timestamp, "deviceinfoid": event.deviceinfoid, "devicedataid": event.devicedataid} for event in events]
    # Get device trend info for last n events
    #last_events = events[-1 * abs(last_n_events):]
    #batteryVoltages = [event.deviceTrendInfo.batteryVoltage for event in last_events]
    #temperatures = [event.deviceTrendInfo.temperature for event in last_events]
    #maxTorques = [event.deviceTrendInfo.maxTorque for event in last_events]
    #strokeTimes = [event.deviceTrendInfo.strokeTime for event in last_events]

    return jsonify({
        "event_datas": event_datas,
        
    })


@api_v1.route("/sensors/<int:sensor_id>/events/<int:event_id>")
@api_v1.route("/sensors/<int:sensor_id>/events/<int:event_id>/hidden")
def event(sensor_id: int, event_id: int):
    """
    Returns a JSON object containing information on a singular sensor event. The `/hidden` may be appended to view the
    data hidden by postprocessing.

    Args:
        sensor_id (int): ID of sensor.
        event_id (int): ID of event.
    """
    isHidden = "hidden" in request.path

    event = _conn.execute_query_readonly(queries.get_event, sensor_id, event_id)

    event_data = format_event_data(event, hide_packet_data=isHidden)
    return jsonify(event_data)


@api_v1.route("/sensors/<int:sensor_id>/events/<int:event_id>/download")
@api_v1.route("/sensors/<int:sensor_id>/events/<int:event_id>/download/hidden")
def event_download(sensor_id, event_id):
    """
    Returns a CSV file containing information on a singular sensor event. The `/hidden` may be appended to view the
    data hidden by postprocessing.

    Args:
        sensor_id (int): ID of sensor.
        event_id (int): ID of event.
    """
    isHidden = "hidden" in request.path
    event_data = fetch_event_data(_conn, sensor_id, event_id)

    # Write CSV without hidden data excluded
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    write_event_csv(csv_writer, event_data, hidden_data=isHidden)

    csv_file.seek(0)
    return Response(
        csv_file.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=event_{sensor_id}_{event_id}_all_packets.csv"}
    )


@api_v1.route("/devices", methods=["GET"])
def devices():
    """
    Returns a JSON object containing a list of devices from the DeviceInfo table.

    Returns:
        JSON: List of devices with their details or an error message if something goes wrong.
    """
    try:
        # Fetch all devices from the database
        devices = _conn.execute_query_readonly(queries.getDevInfo)
        
        # Format the device data
        device_data = [
            {
                "id": device.id,
                "sensorName": device.sensorname,  # Corrected to match the database schema
                "serialNumber": device.serialnumber,  # Corrected
                "deviceType": device.devicetype,  # Corrected
                "deviceLocation": device.devicelocation,  # Corrected
            }
            for device in devices
        ]

        # Return the formatted data as JSON
        return jsonify(device_data), 200

    except Exception as e:
        # Log the error and return a 500 response
        logging.error(f"Error fetching devices: {e}")
        return jsonify({"error": "Failed to fetch devices"}), 500

"""
@api_v1.route("/devices/<int:sensor_id>/events", methods=["GET"])
def device_events(sensor_id: int):
    
    Returns a JSON object containing a list of events, as well as trend data.

    Args:
        sensor_id (int): ID of sensor.
    
    try:
        events = _conn.execute_query_readonly(queries.get_device_events, sensor_id)

        event_data = [
            {
                "id": event.id,
                "timestamp": event.timestamp,
                "deviceDataID": event.devicedataid,
                "deviceInfoID": event.deviceinfoid,
            }
            for event in events
        ]

        return jsonify(event_data), 200

        except Exception as e:
        # Log the error and return a 500 response
        logging.error(f"Error fetching events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500
"""

# Real-time packet updates. Split up for future ease of alterations
def on_heartbeat_packet(sensor_event: SensorEvent):
    _conn.execute_query(queries.upsert_live_sensor_event, sensor_event, 0)


def on_data_packet(sensor_event: SensorEvent):
    _conn.execute_query(queries.upsert_live_sensor_event, sensor_event, 1)


def on_event_summary_packet(sensor_event: SensorEvent, prev_sensor_event: SensorEvent):
    _conn.execute_query(queries.upsert_live_sensor_event, sensor_event, 2, prev_sensor_event)


# Redundant code (deprecated by ThreadedMQTTClient)
def on_message_complete(sensor_event: SensorEvent):
    _conn.execute_query(queries.add_sensor_event, sensor_event)


threaded_client = ThreadedMQTTClient(on_heartbeat_packet, on_data_packet, on_event_summary_packet, on_message_complete)
threaded_client.start()
