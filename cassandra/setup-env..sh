#!/bin/bash

# KAFKA
nohup $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties & > /dev/null && sleep 10
nohup $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties & > /dev/null && sleep 10

$KAFKA_HOME/bin/kafka-topics.sh \
--create \
--zookeeper localhost:2181 \
--replication-factor 1 \
--partitions 1 \
--topic spark-demo-events

# CASSANDRA
nohup $CASSANDRA_HOME/bin/cassandra & > /dev/null && sleep 10

$CASSANDRA_HOME/bin/cqlsh -f scripts/cql/create-table-transactions.cql