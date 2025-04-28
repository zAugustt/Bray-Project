#!/bin/bash

echo_usage() {
    echo "$0 [backend]"
}

test_backend() {
    mkdir -p test_output

    # Build and start the backend container
    docker compose build backend
    docker compose up -d backend
    cid=$(docker ps -q -f name=bray-project-backend-1)

    # Run tests
    docker exec $cid pytest

    # Copy test results
    docker cp "$cid:/app/pytest_report.html" test_output/
    docker cp "$cid:/app/htmlcov" test_output/
    docker compose down
}

# Check the first argument
if [ "$1" == "backend" ]; then
    test_backend
else
    echo "No argument provided."
    echo_usage
fi