# Use the official Eclipse Mosquitto image
FROM eclipse-mosquitto:2

# Set ENV
ARG MQTT_USERNAME
ARG MQTT_PASSWORD

# Expose the default MQTT ports
EXPOSE 1883

# Copy custom configuration file
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Generate passwords file
RUN mosquitto_passwd -c -b /mosquitto/config/passwds ${MQTT_USERNAME} ${MQTT_PASSWORD}
RUN chmod 640 /mosquitto/config/passwds

# Use CMD to start Mosquitto with custom config
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
