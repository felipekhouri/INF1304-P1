# Projeto Kafka Fábrica Inteligente (Simples)

Felipe Khouri Gameleira

## Instalação

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Clone este repositório e entre na pasta `INF1304-P1`.
3. Execute:

```bash
make build
make up

# Após subir o cluster, crie o tópico (3 partições, RF=2):
bash ./cria-topico.sh
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
- Não há persistência em banco de dados, apenas logs.

Para rodar múltiplos consumidores, a forma mais simples é escalar via Compose:

docker-compose up -d --scale consumer=2

Ou, se preferir, duplicar o serviço no `docker-compose.yml`:

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

Para mais detalhes e evidências (logs), veja o `relatorio.txt` e a pasta `evidencias/`.

## Relatório (consolidado)

### 1. Instalação e Uso
- Requisitos: Docker e Docker Compose.
- Passos:
  1) `make build`
  2) `make up`
  3) `bash ./cria-topico.sh` (cria `dados-sensores` com 3 partições e replicação 2)
- Configuração por ambiente: ver `docker-compose.yml` (KAFKA_BOOTSTRAP_SERVERS, TOPIC, GROUP_ID, TEMP_MIN, TEMP_MAX)
- Simulação de falhas: targets do Makefile (stop/start) e `./scripts/simula-falhas.sh`

### 2. Arquitetura
- Zookeeper + 2 brokers Kafka (kafka1, kafka2) com RF=2 para o tópico.
- Produtor Python (sensor) publicando JSON periódico.
- Consumidores Python no mesmo GROUP_ID, com detecção de anomalias e logging.
- Balanceamento de carga por partição e failover automático via rebalance.

### 3. Testes de Falha (como reproduzir)
- Failover de broker: `make stop-broker1 && sleep 10 && make start-broker1` e observar consumo contínuo.
- Rebalance de consumidores: escale com `docker-compose up -d --scale consumer=2`, pare um dos consumidores (`docker stop <nome>`) e observe reassignment.

### 4. Evidências
- Logs de rebalance e consumo: pasta `evidencias/`.
- Referência específica usada na apresentação: `evidencias/rebalance-20251004-2138.log`.
- Alertas gravados em `consumer/alertas.log` durante a execução.

### 5. O que funcionou
- Cluster com replicação; produção/consumo contínuos; rebalance automático.

### 6. Limitações
- Sem persistência/banco e sem dashboard; sem TLS/autenticação (laboratório).

### 7. Decisões de design
- Variáveis de ambiente (sem hard-code); `kafka-python`; tópico com 3 partições.

### 8. Próximos passos
- Persistência (Postgres/InfluxDB), observabilidade (Kafka UI/Prometheus/Grafana), CI.
