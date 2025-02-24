# backend/Dockerfile
# Use an official Python image
FROM python:3.11-alpine

WORKDIR /app

# psycopg2 dependency
RUN apk add postgresql-dev

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
# CMD ["sh", "-c", "python db_connector/populate_data.py && python app.py"]
