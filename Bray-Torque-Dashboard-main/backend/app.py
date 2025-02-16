"""
The `main` file which runs the backend (MQTT Client, API, database connections).

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University

Date:
    November 2024
"""

from flask import Flask
from flask_cors import CORS
from api_v1 import api_v1
import logging

# Start web API
app = Flask(__name__)
CORS(app)

app.register_blueprint(api_v1, url_prefix="/api_v1")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5000)
