# README
The backend consists of 3 major parts:
- MQTT Client (receives and interprets the packet payloads)
- REST API (provides data for frontend)
- Database Connector (manages interactions with database)

To run the backend with Docker:
```bash
# If you have not built the Docker images or made changes to the codebase
docker compose build backend

# Then
docker compose up -d backend
```

## Docker
This program currently is meant to run alongside the other Docker containers defined in the [Docker Compose](../docker-compose.yml). The Dockerfile for the backend can be seen [here](Dockerfile). 

## [Database Connector](db_connector/)
This module provides connections to the database, and ways to query (with rollbacks if those queries fail). This is used by both the MQTT client and API.

## [MQTT Client](mqtt_client/)
The client expects that packet payloads will be sent with the topic format `/sensor/<devEUI>/port/<portNumber>`. \
The topic format can be modified in the gateway or other source publishing messages to the broker.

This client subscribes to the MQTT broker created by Docker, parsing the data received and inserting this into the database. If an event already exists in the database, it will update the event with the new information in that packet.

## [REST API](api_v1/)
This API provides Flask endpoints for the frontend to query. A full list of endpoints can be found in the [module header](api_v1/__init__.py). The route prefix is `api_v1`, which means that an endpoint like `/sensors` becomes `/api_v1/sensors`.

## Entrypoint
If looking at where to start analyzing this code, start from [app.py](app.py).
