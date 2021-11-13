import json
import os
import time
from concurrent import futures
from kafka import KafkaProducer

import grpc

import location_pb2
import location_pb2_grpc

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

        request_value = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude),
            "creation_time": request.creation_time
        }

        json_data = json.dumps(request_value).encode('utf-8')

        producer.send(KAFKA_TOPIC, json_data)

        producer.flush()

        return location_pb2.LocationMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("127.0.0.1:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)