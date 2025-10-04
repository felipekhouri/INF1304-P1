# Projeto Kafka Fábrica Inteligente (Simples)

Felipe Khouri Gameleira

## Instalação

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Clone este repositório e entre na pasta `INF1304-P1`.
3. Execute:

```bash
make build
make up

# Após subir o cluster, crie o tópico com:
./cria-topico.sh
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

Script auxiliar (opcional):
- `./scripts/simula-falhas.sh broker1 stop` (ou `broker2`, `consumer`, use `start` para subir novamente). O script acompanha logs do consumidor para evidenciar eventos de "Rebalance".

## Logs
- Veja os logs de todos os serviços:
  - `make logs`
 - Alertas do consumidor ficam em `consumer/alertas.log`.

## Observação
- O sensor envia dados aleatórios de temperatura e vibração a cada 2 segundos.
- O consumidor detecta anomalias de temperatura (>80 ou <10).
- O balanceamento de carga e failover podem ser observados parando/voltando serviços.

Configuração via variáveis de ambiente:
- `KAFKA_BOOTSTRAP_SERVERS` (sensor/consumer)
- `TOPIC` (sensor/consumer)
- `GROUP_ID`, `TEMP_MIN`, `TEMP_MAX` (consumer)

## Limitações
- Projeto simplificado para entrega rápida.
- Não há persistência em banco de dados, apenas logs.

Para rodar múltiplos consumidores, basta duplicar o serviço no `docker-compose.yml`:

  consumer2:
    build: ./consumer
    environment:
      KAFKA_BOOTSTRAP_SERVERS: kafka1:9092,kafka2:9093
      TOPIC: dados-sensores
      GROUP_ID: grupo-consumidor
      TEMP_MIN: "10"
      TEMP_MAX: "80"
    depends_on:
      - kafka1
      - kafka2

Ou rode manualmente outro container:

docker-compose run --rm consumer

Os logs de rebalanceamento podem ser vistos ao rodar dois consumidores e parar um deles.

## Arquitetura (resumo)

[sensor] ---> [Kafka (broker1, broker2)] ---> [consumer1, consumer2]

- Sensores produzem dados para o tópico `dados-sensores`.
- Consumidores compartilham a carga (cada um lê partições diferentes) no mesmo `GROUP_ID`.
- Se um consumidor cai, outro assume sua partição automaticamente (rebalanceamento).

Para mais detalhes, veja o `relatorio.txt`.
