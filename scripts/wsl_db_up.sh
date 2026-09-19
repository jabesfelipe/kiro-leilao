#!/usr/bin/env bash
# Sobe o Postgres+pgvector no Docker (WSL) e aguarda ficar saudável.
# Uso (no WSL):  bash scripts/wsl_db_up.sh
set -uo pipefail

# docker instalado via snap fica em /snap/bin (fora do PATH em shells não-login)
export PATH="/snap/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

cd "$(dirname "$0")/.."

echo "== subindo container =="
docker compose up -d db

echo "== aguardando healthcheck =="
for i in $(seq 1 40); do
  status=$(docker inspect -f '{{.State.Health.Status}}' radar_db 2>/dev/null || echo "n/a")
  echo "  tentativa $i: $status"
  if [ "$status" = "healthy" ]; then break; fi
  sleep 3
done

echo "== versao do servidor =="
docker exec radar_db psql -U radar -d radar -tAc "select version();" | head -1

echo "== pgvector disponivel? =="
docker exec radar_db psql -U radar -d radar -tAc \
  "select count(*) from pg_available_extensions where name='vector';"

echo "== habilitando extensao vector =="
docker exec radar_db psql -U radar -d radar -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "== pgvector instalado? =="
docker exec radar_db psql -U radar -d radar -tAc \
  "select extversion from pg_extension where extname='vector';"

echo "OK"
