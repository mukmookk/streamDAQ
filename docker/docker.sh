#!/bin/bash

# Define the names of the containers
KAFKA_CONTAINER_NAME="my-kafka"
CASSANDRA_CONTAINER_NAME="my-cassandra"

# Define the network name
NETWORK_NAME="my-network"

# Create a Docker network
docker network create $NETWORK_NAME

# Start the Kafka container
docker run -d --name $KAFKA_CONTAINER_NAME --network $NETWORK_NAME -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=$KAFKA_CONTAINER_NAME wurstmeister/kafka:2.12-2.3.0

# Wait for Kafka to start up
sleep 10

# Start the Cassandra container
docker run -d --name $CASSANDRA_CONTAINER_NAME --network $NETWORK_NAME -p 9042:9042 cassandra:3.11

# Wait for Cassandra to start up
sleep 10

# Create the Kafka topics
docker exec -it $KAFKA_CONTAINER_NAME /opt/kafka/bin/kafka-topics.sh --create --zookeeper $KAFKA_CONTAINER_NAME:2181 --replication-factor 1 --partitions 1 --topic my-topic

# Display the status of the containers
docker ps