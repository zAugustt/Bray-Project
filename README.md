# README

## Introduction

Website that displays a device list and corresponding event histories.

Provides:
- Torque graphs for sensor events
- Trend data for valve performance
- Event history for sensors
- List of all sensors

## Developer Note:
### Database Migration
- Inside the `backend` Docker container, run `alembic upgrade head`

## Requirements

This code has been run and tested using the following internal and external components

Environment
- Any hardware/operating system capable of running x86 64 bit Docker containers (Tested using Windows 10/11 and Ubuntu  24.04.1)
- Docker Engine 27.3.1

Programs
- Front-end container: [node:18-alpine](<https://hub.docker.com/layers/library/node/18-alpine/images/sha256-ea8e360a721d870337fe899c70ea7def62f2a72cf1b6f7beb8a3ccaac8b6049c>)
    - npm 10.7.0
- Back-end container: [python:3.11-alpine](<https://hub.docker.com/layers/library/python/3.11-alpine/images/sha256-851e1d6a857c7e3b43d1bac73f307140a980c267ba216deae4dcbdb057096134>)
    - Python 3.11.10
    - Flask 3.0.3
    - Werkzeug 3.0.4
- Database (Postgres) container: [node:18-alpine](<https://hub.docker.com/layers/library/postgres/13-alpine/images/sha256-0658c4f5521f043f62d7e3431ad523261b9108ecbfb3f58a2350ac4e29ce1147>)
    - PostgreSQL 13.16
- MQTT (Mosquitto) container: [eclipse-mosquitto:2](<https://hub.docker.com/layers/library/eclipse-mosquitto/2/images/sha256-4a46c840adf48e7acd49883206a5c075c14ec95845ee6d30ba935a6719d6b41c>)
    - mosquitto 2.0.20

Tools
- GitHub
- Jira
- Git

## External Deps

- Docker - Download latest version at https://www.docker.com/products/docker-desktop
- Git - Downloat latest version at https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- GitHub Desktop (Not needed, but HELPFUL) at https://desktop.github.com/

## Documentation

Our product and sprint backlog can be found in Jira, with project name "Bray Capstone Project"

The team is storing all documnetation within Confluence. More documentation is in progress. Current structure:

Confluence
- Project Documentation
    - LoRa Models
    - Bray Provided Documentation List
    - Dashboard LoFi Prototype
    - Dashboard Model

- Analysis:
    - Analysis - Dynamic Packet Size
    - Analysis - Change Data Resolution
    - Analysis - EEPROM Connection:
    - Analysis - Isolate Stroke Length
    - Analysis - Dashboard Tech Stack

## Installation

Download this code repository by using git:

`git clone https://github.com/Trans-Opt/Bray-Torque-Dashboard.git`

## Tests

Run `./test.sh backend` to run the functional tests on the backend

## Execute Code

Run the following code in Powershell if using windows or the terminal using Linux/Mac

- Run `npm install` locally prior to the following to expedite react install times or to run locally w/o Docker
    - Run `npm start` after `npm install` to run the app locally without Docker
---
- Use `docker compose up -d` to start
- Use `docker compose down`
    - Run `docker compose down --rmi all` to remove images and volumes associated with this compose
        - Also useful when code changes don't reflect on the front end


The application can be seen using a browser and navigating to http://localhost:3001/


## Environmental Variables/Files

Environment variables to set:
- `POSTGRES_PASSWORD`

## Deployment

1. Deployment Docker images will be created through the GitHub pipeline. 
2. Alternative to running the premade images:
    - Ensure that you have instantiated the environment variables in the `Environmental Variables/Files` section of the README. 
    - Follow the `Execute Code` step of the README.

## CI/CD

GitHub Actions pipeline in progress.

## Support

Development of the website is currently in progress with minimal features implemented. Support will be provided until the end of the 2024 Fall school semester (December 2024).

## Extra Help

Please contact Pauline Wade paulinewade@tamu.edu for any questions related to the website.

## References ##

N/A