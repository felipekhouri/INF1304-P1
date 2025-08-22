"""
Consumidor Kafka para o tópico 'dados-sensores'.
Detecta anomalias de temperatura e salva alertas em arquivo de log.
Mostra a partição de cada mensagem recebida.
"""
from kafka import KafkaConsumer
import json
import os
import logging

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC = os.getenv('TOPIC', 'dados-sensores')

# Configura logger para salvar alertas
logging.basicConfig(filename='alertas.log', level=logging.INFO, format='%(asctime)s %(message)s')

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='grupo-consumidor',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

def detect_anomaly(data):
    """
    Retorna True se a temperatura estiver fora dos limites (10-80).
    """
    temp = data.get('temperatura', 0)
    if temp > 80 or temp < 10:
        return True
    return False

if __name__ == '__main__':
    print("Consumidor iniciado. Aguardando mensagens...")
    for msg in consumer:
        data = msg.value
        part = msg.partition
        if detect_anomaly(data):
            alerta = f"[ALERTA] Anomalia detectada na partição {part}: {data}"
            print(alerta)
            logging.info(alerta)
        else:
            print(f"Recebido da partição {part}: {data}")
