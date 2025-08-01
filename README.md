# Projeto Kafka Fábrica Inteligente (Simples)

## Instalação

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Clone este repositório e entre na pasta `meuprojeto`.
3. Execute:

```bash
make build
make up
```

## Componentes
- 2 brokers Kafka + 1 Zookeeper
- 1 sensor (produtor) Python
- 1 consumidor Python

## Como simular falhas
- Parar um broker:
  - `make stop-broker1` ou `make stop-broker2`
- Parar o consumidor:
  - `make stop-consumer`
- Reiniciar serviços:
  - `make start-broker1`, `make start-broker2`, `make start-consumer`

## Logs
- Veja os logs de todos os serviços:
  - `make logs`

## Observação
- O sensor envia dados aleatórios de temperatura e vibração a cada 2 segundos.
- O consumidor detecta anomalias de temperatura (>80 ou <10).
- O balanceamento de carga e failover podem ser observados parando/voltando serviços.

## Limitações
- Projeto simplificado para entrega rápida.
- Não há persistência em banco de dados, apenas logs.

# Para rodar múltiplos consumidores, basta duplicar o serviço no docker-compose.yml:
#
#  consumer2:
#    build: ./consumer
#    environment:
#      KAFKA_BOOTSTRAP_SERVERS: kafka1:9092,kafka2:9093
#      TOPIC: dados-sensores
#    depends_on:
#      - kafka1
#      - kafka2
#
# Ou rode manualmente outro container:
# docker-compose run --rm consumer

# Após subir o cluster, crie o tópico com:
# ./cria-topico.sh

# Os logs de rebalanceamento podem ser vistos ao rodar dois consumidores e parar um deles.

# Exemplo de arquitetura:
#
# [sensor] ---> [Kafka (broker1, broker2)] ---> [consumer1, consumer2]
#
# - Sensores produzem dados para o tópico 'dados-sensores'.
# - Consumidores compartilham a carga (cada um lê partições diferentes).
# - Se um consumidor cai, outro assume sua partição automaticamente.

# Para mais detalhes, veja o relatorio.txt.
