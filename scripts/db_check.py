"""Verifica conexão com o banco e disponibilidade de pgvector.

Uso: python scripts/db_check.py
Lê as credenciais de RADAR_DATABASE_URL (arquivo .env).
"""

from __future__ import annotations

import sys

import psycopg

# carrega .env manualmente (sem dependências extras)
from pathlib import Path


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = Path(__file__).resolve().parents[1] / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def to_libpq(url: str) -> str:
    """Converte SQLAlchemy URL (postgresql+psycopg://...) para DSN libpq."""
    return url.replace("postgresql+psycopg://", "postgresql://")


def main() -> int:
    env = load_env()
    url = env.get("RADAR_DATABASE_URL", "")
    schema = env.get("RADAR_DB_SCHEMA", "poc_ia")
    if not url:
        print("RADAR_DATABASE_URL não definida no .env")
        return 1

    dsn = to_libpq(url)
    # RDS em VPC privada: o hostname público não resolve fora da VPC, mas o IP
    # privado é alcançável via VPN. Se RADAR_DB_HOST_ADDR estiver setado, força o IP
    # (mantendo sslmode=require para criptografar sem validar CN — adequado a dev).
    host_addr = env.get("RADAR_DB_HOST_ADDR")
    if host_addr:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}hostaddr={host_addr}&sslmode=require"

    try:
        with psycopg.connect(dsn, connect_timeout=15) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                ver = cur.fetchone()[0]
                print("Conectado:", ver.split(",")[0])

                cur.execute("SELECT current_database(), current_user;")
                db, user = cur.fetchone()
                print(f"Banco: {db} | Usuário: {user}")

                # pgvector disponível para instalação?
                cur.execute("SELECT 1 FROM pg_available_extensions WHERE name = 'vector';")
                available = cur.fetchone() is not None
                print(f"pgvector disponível: {available}")

                cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
                installed = cur.fetchone() is not None
                print(f"pgvector instalado: {installed}")

                cur.execute(
                    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s;",
                    (schema,),
                )
                exists = cur.fetchone() is not None
                print(f"Schema '{schema}' existe: {exists}")
        return 0
    except Exception as e:  # noqa: BLE001
        print("ERRO ao conectar:", type(e).__name__, str(e)[:300])
        return 2


if __name__ == "__main__":
    sys.exit(main())
