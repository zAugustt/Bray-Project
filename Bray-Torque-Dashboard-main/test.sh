#!/bin/bash

echo_usage() {
    echo "$0 [backend]"
}

test_backend() {
    mkdir -p test_output

    docker compose build backend
    docker compose up -d backend
    cid=$(docker ps -q -f name=bray-torque-dashboard-main-backend-1)
    echo "CID: $cid";
    docker exec $cid pytest
    docker cp "$cid:/app/pytest_report.html" test_output/
    docker cp "$cid:/app/htmlcov" test_output
    docker compose down
}

# Check if the first argument is "backend"
if [ "$1" == "backend" ]; then
    test_backend
else
    echo_usage
fi
