"""
Standalone python file meant for debugging purposes. This program is meant to interpret a list of data files in a
folder, with a couple of options (selected by modifying the `main` function):
- Displaying the torque data in a graph
- Displaying the torque data of 2 strokes on the same graph
- Adding the stroke data to the database

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University

Date:
    November 2024
"""

import sys, os
from mqtt_client import SensorEvent
import logging


SEARCH_DIR = "mqtt_client/data"


def display(data_packets, folder_name):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(10, 5))
    
    colors = plt.cm.jet(np.linspace(0, 1, len(data_packets)))
    
    start_index = 0
    for i, packet in enumerate(data_packets):
        if packet is not None:
            end_index = start_index + len(packet)
            plt.plot(range(start_index, end_index), packet, marker='o', linestyle='-', color=colors[i], markersize=4)
            start_index = end_index 

    plt.title(folder_name)
    plt.xlabel('Index')
    plt.ylabel('microvolt')
    # plt.savefig(f"{folder_name}_plot.png")
    plt.show()


def add_to_db(sensor_event):
    from db_connector import DBConnector
    from db_connector import queries
    _conn = DBConnector()
    _conn.execute_query(queries.create_tables)
    _conn.execute_query(queries.add_sensor_event, sensor_event)


def dump_data():
    folder = sys.argv[1]
    folder_path = os.path.join(SEARCH_DIR, folder)


    event = SensorEvent()

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if not os.path.isfile(filepath):
            continue

        _, _, name, filetype = filename.split(".")
        topic = "/".join(name.split("_"))

        event.parse_from_data(topic, open(filepath, "rb").read())

    print(event)
    print(f"{event.torqueData = }")
    print(f"Data packets: {len(event.torqueData)}")

    data = []
    for i, seq in enumerate(event.torqueData):
        if seq is None:
            print(f"WARNING!!!!!!!!!! Missing seq packet #{i+1}!")
            seq = []
        data.extend(seq)
    print(f"Data points: {len(data)}")

    display(event.torqueData, folder)
    # add_to_db(event)


def test_mqtt_client():
    from mqtt_client import ThreadedMQTTClient
    from time import sleep

    client = ThreadedMQTTClient()
    client.start()

    sleep(60)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    dump_data()
