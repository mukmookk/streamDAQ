#!/bin/bash

export WORKDIR=$(pwd)

# Stop and remove existing Kafka containers
docker-compose -f $WORKDIR/kafka.yml down

# Start Kafka containers in detached mode
docker-compose -f $WORKDIR/kafka.yml up -d

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
docker-compose exec kafka kafka-topics.sh --list >/dev/null 2>&1
while [ $? -ne 0 ]
do
  sleep 1
  docker-compose exec kafka kafka-topics.sh --list >/dev/null 2>&1
done
echo "Kafka is ready!"

# Create a new Kafka topic
docker-compose exec kafka kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic nasdaq

# Start a Kafka consumer to listen for messages on the new topic
docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic nasdaq --from-beginning