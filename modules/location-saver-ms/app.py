import json
import os
from app.models import Location  # noqa
from app.services import LocationService
from kafka import KafkaConsumer

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER)

while True:
    for message in consumer:
        request = message.value.decode('utf-8')
        location = json.loads(request)
        LocationService.create(location)
