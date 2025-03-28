# Kafka bash commands to interact with the kafka apis

## Connecting to Docker in Exec Mode

Before using the Kafka commands, you need to connect to the Docker container running Kafka in exec mode. This allows you to interact with the Kafka APIs directly from within the container.

To start, run the following command to access the Kafka container:

```bash
docker exec -it kafka sh
```

This command opens a shell session inside the Kafka container, enabling you to execute the Kafka commands.

You can use below commands to test out the kafka functionality and use it as a cheat sheet.

1. Create a Topic with Multiple Partitions and a Replication Factor
```bash
./bin/kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 2
```

Check the topic’s details (partitions, replication factor, etc.):

```bash
./bin/kafka-topics.sh --describe \
  --topic my-topic \
  --bootstrap-server localhost:9092
```

2. Test the Producer by Sending Messages
```bash
./bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic
```

3. Test the Consumer: Reading Messages from the Beginning
```bash
./bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group consumer-group-1 \
  --from-beginning
```

4. Testing Consumer Groups and Fan-Out Behavior
```bash 
./bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group consumer-group-1 \
  --from-beginning
```
5. **Across Different Consumer Groups:**
```bash
./bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group consumer-group-2 \
  --from-beginning
```

6. Testing Additional Use Cases
```bash
cat messages.txt | ./bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic
```
7. observing the behavior of the file 
```bash 
./bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group consumer-group-3
```