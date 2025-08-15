"""
Produtor Kafka que simula sensores enviando dados periódicos.
Gera temperatura e vibração aleatórias e envia para o tópico definido por variável de ambiente.
"""

from kafka import KafkaProducer
import json
import os
import random
import time

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC = os.getenv('TOPIC', 'dados-sensores')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    """
    Gera um dicionário simulando dados de um sensor.
    """
    return {
        'sensor_id': f'sensor-{random.randint(1, 100)}',
        'temperatura': round(random.uniform(5, 100), 2),
        'vibracao': round(random.uniform(0, 10), 2),
        'timestamp': int(time.time())
    }

if __name__ == '__main__':
    print("Sensor iniciado. Enviando dados...")
    while True:
        data = generate_sensor_data()
        producer.send(TOPIC, data)
        print(f"Enviado: {data}")
        time.sleep(2)
