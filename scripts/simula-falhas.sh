#!/usr/bin/env bash
set -euo pipefail

# Script de simulação de falhas e observação de rebalanceamento.
# Uso:
#   ./scripts/simula-falhas.sh broker1|broker2|consumer [stop|start]

SERVICE=${1:-}
ACTION=${2:-stop}

if [[ -z "$SERVICE" ]]; then
  echo "Uso: $0 broker1|broker2|consumer [stop|start]" >&2
  exit 1
fi

case "$SERVICE" in
  broker1) NAME=kafka1 ;;
  broker2) NAME=kafka2 ;;
  consumer) NAME=consumer ;;
  *) echo "Serviço inválido: $SERVICE" >&2 ; exit 1 ;;
esac

if [[ "$ACTION" == "stop" ]]; then
  echo "Parando $NAME..."
  docker-compose stop "$NAME"
  echo "Aguardando 10s e acompanhando logs para ver rebalanceamento..."
  sleep 10
  docker-compose logs -f consumer | sed -n '/Rebalance/,$p'
else
  echo "Iniciando $NAME..."
  docker-compose start "$NAME"
  echo "Aguardando 10s e acompanhando logs para ver rebalanceamento..."
  sleep 10
  docker-compose logs -f consumer | sed -n '/Rebalance/,$p'
fi
