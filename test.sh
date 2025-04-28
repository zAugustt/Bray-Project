#!/bin/bash

echo_usage() {
    echo "$0 [all|db_connector|mqtt|api]"
}

test_db_connector() {
    echo "Running tests for db_connector..."
    mkdir -p test_output/db_connector_htmlcov

    # Start test database
    docker compose up -d db_test
    until docker exec bray-project-db_test-1 pg_isready -U test_user; do
        echo "Waiting for PostgreSQL test database to be ready..."
        sleep 2
    done

    echo "Building and starting backend..."
    docker compose build backend
    docker compose up -d backend

    cid=$(docker ps -q -f name=bray-project-backend-1)

    if [ -z "$cid" ]; then
        echo "Error: Backend container did not start properly."
        docker compose logs backend
        exit 1
    fi

    docker exec $cid pytest tests/test_db_connector.py --cov=db_connector --cov-report=html --cov-report=xml:db_connector_coverage.xml --cov-fail-under=90

    docker cp "$cid:/app/htmlcov" test_output/db_connector_htmlcov
    docker cp "$cid:/app/db_connector_coverage.xml" test_output/db_connector_coverage.xml

    docker compose down
}

test_mqtt() {
    echo "Running tests for mqtt_client..."
    mkdir -p test_output/mqtt_htmlcov

    echo "Building and starting backend..."
    docker compose build backend
    docker compose up -d backend

    cid=$(docker ps -q -f name=bray-project-backend-1)

    if [ -z "$cid" ]; then
        echo "Error: Backend container did not start properly."
        docker compose logs backend
        exit 1
    fi

    docker exec $cid pytest --cov=mqtt_client tests/test_mqtt_client.py --cov-report=html --cov-fail-under=90
    

    docker cp "$cid:/app/htmlcov" test_output/mqtt_htmlcov
    docker cp "$cid:/app/mqtt_coverage.xml" test_output/mqtt_coverage.xml

    docker compose down
}

test_api() {
    echo "Running tests for api_v1..."
    mkdir -p test_output/api_htmlcov

    echo "Building and starting backend..."
    docker compose build backend
    docker compose up -d backend

    cid=$(docker ps -q -f name=bray-project-backend-1)

    if [ -z "$cid" ]; then
        echo "Error: Backend container did not start properly."
        docker compose logs backend
        exit 1
    fi

    docker exec $cid pytest tests/test_api.py --cov=api_v1 --cov-report=html --cov-report=xml:api_coverage.xml --cov-fail-under=90

    docker cp "$cid:/app/htmlcov" test_output/api_htmlcov
    docker cp "$cid:/app/api_coverage.xml" test_output/api_coverage.xml

    docker compose down
}

test_all() {
    mkdir -p test_output/combined

    # Run all separate parts
    test_db_connector
    test_mqtt
    test_api

    echo "Combining coverage reports..."

    echo "Building and starting backend..."
    docker compose build backend
    docker compose up -d backend

    cid=$(docker ps -q -f name=bray-project-backend-1)

    if [ -z "$cid" ]; then
        echo "Error: Backend container did not start properly."
        docker compose logs backend
        exit 1
    fi

    docker exec $cid bash -c "
        pip install coverage &&
        mkdir -p combined_coverage &&
        coverage combine db_connector_coverage.xml mqtt_coverage.xml api_coverage.xml &&
        coverage html -d combined_coverage &&
        cp -r combined_coverage /app/test_output/combined
    "

    docker cp "$cid:/app/test_output/combined" test_output/combined_htmlcov

    docker compose down

    echo "Combined full coverage report is in test_output/combined_htmlcov/"
}

# Command dispatcher
if [ "$1" == "db_connector" ]; then
    test_db_connector
elif [ "$1" == "mqtt" ]; then
    test_mqtt
elif [ "$1" == "api" ]; then
    test_api
elif [ "$1" == "all" ]; then
    test_all
else
    echo "No argument provided."
    echo_usage
fi
