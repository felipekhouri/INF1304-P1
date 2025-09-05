#!/bin/bash
# Cria o tópico 'dados-sensores' com 3 partições e fator de replicação 2
# Execute após subir o cluster (make up)

KAFKA_CONTAINER=kafka1
TOPIC=dados-sensores
PARTITIONS=3
REPLICATION=2

# Aguarda Kafka subir
sleep 10

docker-compose exec $KAFKA_CONTAINER kafka-topics \
  --create \
  --topic $TOPIC \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION \
  --if-not-exists \
  --bootstrap-server kafka1:9092,kafka2:9093

echo "Tópico '$TOPIC' criado com $PARTITIONS partições e replicação $REPLICATION."
