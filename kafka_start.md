To check if a Kafka server is running, you can use the following steps:

1. Open a terminal window or command prompt.

2. Navigate to the Kafka installation directory.

3. Run the following command to start ZooKeeper:
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
4. Open a new terminal window or command prompt.

5. Navigate to the Kafka installation directory.

6. Run the following command to start Kafka:
```
bin/kafka-server-start.sh config/server.properties
```
7. Wait for the Kafka server to start up.

8. To check if the Kafka server is running, you can use the following command:
```
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

This command will list all the topics in the Kafka cluster. If you see the list of topics, then the Kafka server is up and running. If you get an error message, then the Kafka server may not be running or there may be an issue with your configuration.

----
### Port 9092 vs 2181

Port 9092 is used for communication between Kafka clients and Kafka brokers. This is the default port used by Kafka for its message transfer protocol (TCP), and it's where Kafka clients send and receive messages to/from the Kafka brokers.

On the other hand, port 2181 (not 2191) is used for communication between Kafka and ZooKeeper. ZooKeeper is used by Kafka to maintain cluster coordination and metadata management. Kafka brokers register themselves with ZooKeeper, and Kafka clients use ZooKeeper to discover the Kafka brokers and to maintain their session state.

So, in summary, port 9092 is used for communication between Kafka clients and Kafka brokers, while port 2181 is used for communication between Kafka and ZooKeeper.