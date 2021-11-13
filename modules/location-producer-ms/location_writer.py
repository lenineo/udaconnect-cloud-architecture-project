import grpc
import location_pb2
import location_pb2_grpc

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# create location message for test
location_message = location_pb2.LocationMessage(
    person_id=1,
    longitude='123',
    latitude='233',
    creation_time='2021-11-01T12:00:00'
)

print("Sending location by gRPC...")

response = stub.Create(location_message)

print(response)