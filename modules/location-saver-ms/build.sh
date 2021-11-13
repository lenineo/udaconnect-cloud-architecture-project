#!/usr/bin/sh

docker build -t ulyanov/location-producer-ms:v1 .
docker push ulyanov/location-producer-ms:v1
