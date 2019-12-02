FROM python:alpine3.6
COPY . /app
WORKDIR /app
RUN pip install paho-mqtt
CMD python ./mqtt_client_for_mosquitto.py
