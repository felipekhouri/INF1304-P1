"""
Consumidor Kafka para o tópico 'dados-sensores'.

Funcionalidades:
- Detecta anomalias de temperatura e salva alertas em arquivo de log.
- Mostra a partição de cada mensagem recebida.

Configuração via variáveis de ambiente (evita hard-code):
- KAFKA_BOOTSTRAP_SERVERS: lista de brokers (ex: "kafka1:9092,kafka2:9093").
- TOPIC: nome do tópico (ex: "dados-sensores").
- GROUP_ID: id do grupo de consumidores (default: "grupo-consumidor").
- TEMP_MIN: limite inferior da faixa normal de temperatura (default: 10).
- TEMP_MAX: limite superior da faixa normal de temperatura (default: 80).
"""
from kafka import KafkaConsumer
import json
import os
import logging

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC = os.getenv('TOPIC', 'dados-sensores')
GROUP_ID = os.getenv('GROUP_ID', 'grupo-consumidor')
TEMP_MIN = float(os.getenv('TEMP_MIN', '10'))
TEMP_MAX = float(os.getenv('TEMP_MAX', '80'))

# Configura logger para salvar alertas
logging.basicConfig(filename='alertas.log', level=logging.INFO, format='%(asctime)s %(message)s')

class RebalanceLogger:
    """Listener para logar eventos de rebalanceamento de partições."""

    def on_partitions_revoked(self, revoked):
        parts = ", ".join(str(p) for p in revoked) if revoked else "(nenhuma)"
        msg = f"Rebalance: partições revogadas: {parts}"
        print(msg)
        logging.info(msg)

    def on_partitions_assigned(self, assigned):
        parts = ", ".join(str(p) for p in assigned) if assigned else "(nenhuma)"
        msg = f"Rebalance: partições atribuídas: {parts}"
        print(msg)
        logging.info(msg)

consumer = KafkaConsumer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id=GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True
)
consumer.subscribe([TOPIC], listener=RebalanceLogger())

def detect_anomaly(data):
    """
    Retorna True se a temperatura estiver fora dos limites configurados (TEMP_MIN - TEMP_MAX).
    """
    temp = data.get('temperatura', 0)
    return temp > TEMP_MAX or temp < TEMP_MIN

if __name__ == '__main__':
    print(
        f"Consumidor iniciado. Bootstrap: {KAFKA_BOOTSTRAP_SERVERS} | "
        f"Tópico: {TOPIC} | Grupo: {GROUP_ID} | Limites: {TEMP_MIN}-{TEMP_MAX}"
    )
    for msg in consumer:
        data = msg.value
        part = msg.partition
        if detect_anomaly(data):
            alerta = f"[ALERTA] Anomalia detectada na partição {part}: {data}"
            print(alerta)
            logging.info(alerta)
        else:
            print(f"Recebido da partição {part}: {data}")
