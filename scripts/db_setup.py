"""Aplica o schema (db/schema.sql) no banco configurado. Idempotente e portável.

Uso:
    python scripts/db_setup.py            # cria schema/extensão/tabelas (tolera "já existe")
    python scripts/db_setup.py --drop     # DROP SCHEMA poc_ia CASCADE antes de recriar

Lê credenciais de .env (RADAR_DATABASE_URL, RADAR_DB_SCHEMA, RADAR_DB_HOST_ADDR).
Funciona tanto no RDS provisório (via IP) quanto em Postgres local (só trocar o .env).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[1]

# erros que significam "objeto já existe" — seguros de ignorar num setup idempotente
DUPLICATE_SQLSTATES = {
    "42710",  # duplicate_object (type, extension)
    "42P07",  # duplicate_table
    "42P06",  # duplicate_schema
    "42723",  # duplicate_function
    "42P16",  # invalid_table_definition (índice duplicado em alguns casos)
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def build_dsn(env: dict[str, str]) -> str:
    dsn = env.get("RADAR_DATABASE_URL", "").replace("postgresql+psycopg://", "postgresql://")
    host_addr = env.get("RADAR_DB_HOST_ADDR")
    if host_addr:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}hostaddr={host_addr}&sslmode=require"
    return dsn


def split_statements(sql: str) -> list[str]:
    """Divide o SQL em statements por ';' no fim de linha, ignorando comentários.

    Suficiente para este schema (sem funções/DO com ';' interno).
    """
    # remove comentários inline (-- ... até o fim da linha), preservando literais.
    # Suficiente para este schema (não há '--' dentro de strings).
    clean_lines = []
    for ln in sql.splitlines():
        idx = ln.find("--")
        clean_lines.append(ln if idx == -1 else ln[:idx])
    body = "\n".join(clean_lines)
    parts = [s.strip() for s in body.split(";")]
    return [p for p in parts if p]


def main() -> int:
    env = load_env()
    schema = env.get("RADAR_DB_SCHEMA", "poc_ia")
    dsn = build_dsn(env)
    if not dsn:
        print("RADAR_DATABASE_URL não definida no .env")
        return 1

    do_drop = "--drop" in sys.argv
    sql = (ROOT / "db" / "schema.sql").read_text(encoding="utf-8")
    statements = split_statements(sql)

    applied = 0
    skipped = 0
    try:
        with psycopg.connect(dsn, connect_timeout=20, autocommit=True) as conn:
            with conn.cursor() as cur:
                if do_drop:
                    print(f"DROP SCHEMA {schema} CASCADE...")
                    cur.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")

                # a extensão pgvector pode exigir rds_superuser; se já existir, ok
                cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
                has_vector = cur.fetchone() is not None

                for stmt in statements:
                    is_vector_ext = "CREATE EXTENSION" in stmt and "vector" in stmt
                    try:
                        cur.execute(stmt)
                        applied += 1
                    except psycopg.errors.Error as e:  # noqa: PERF203
                        state = getattr(e, "sqlstate", None)
                        if state in DUPLICATE_SQLSTATES:
                            skipped += 1
                        elif is_vector_ext and state == "42501" and not has_vector:
                            # sem privilégio para criar a extensão: avisa e segue.
                            # A coluna VECTOR será criada só quando 'vector' for habilitada
                            # por um rds_superuser (CREATE EXTENSION vector;).
                            print(
                                "AVISO: sem privilégio para criar extensão 'vector'. "
                                "Peça a um rds_superuser: CREATE EXTENSION vector; "
                                "Prosseguindo sem a coluna de embedding."
                            )
                            skipped += 1
                        elif "VECTOR(1536)" in stmt.upper() and not has_vector:
                            # tabela document_chunks depende do tipo vector; recria sem embedding
                            fallback = re.sub(
                                r",?\s*embedding\s+VECTOR\(1536\)", "", stmt, flags=re.IGNORECASE
                            )
                            try:
                                cur.execute(fallback)
                                applied += 1
                                print("AVISO: document_chunks criada SEM coluna 'embedding' "
                                      "(pgvector indisponível). Adicionar depois via ALTER TABLE.")
                            except psycopg.errors.Error as e2:
                                if getattr(e2, "sqlstate", None) in DUPLICATE_SQLSTATES:
                                    skipped += 1
                                else:
                                    print(f"FALHA (fallback): {e2}")
                                    return 2
                        elif is_vector_ext or ("ivfflat" in stmt.lower() and not has_vector):
                            # índice IVFFlat também depende de pgvector
                            skipped += 1
                        else:
                            head = re.sub(r"\s+", " ", stmt)[:80]
                            print(f"FALHA no statement: {head}...\n  {state}: {e}")
                            return 2

                # convergência: se pgvector existe mas a coluna embedding não,
                # adiciona agora (cobre bancos criados antes da extensão existir).
                cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
                if cur.fetchone() is not None:
                    cur.execute(
                        "SELECT 1 FROM information_schema.columns "
                        "WHERE table_schema = %s AND table_name = 'document_chunks' "
                        "AND column_name = 'embedding';",
                        (schema,),
                    )
                    if cur.fetchone() is None:
                        cur.execute(
                            f"ALTER TABLE {schema}.document_chunks "
                            "ADD COLUMN embedding VECTOR(1536);"
                        )
                        cur.execute(
                            f"CREATE INDEX IF NOT EXISTS idx_chunks_embedding "
                            f"ON {schema}.document_chunks "
                            "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"
                        )
                        print("Coluna 'embedding' e índice IVFFlat adicionados.")

                # relatório final
                cur.execute(
                    "SELECT count(*) FROM information_schema.tables WHERE table_schema = %s;",
                    (schema,),
                )
                tables = cur.fetchone()[0]
                cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
                pgvector = cur.fetchone() is not None

        print(f"OK. statements aplicados={applied} ignorados(já existiam)={skipped}")
        print(f"Tabelas no schema '{schema}': {tables} | pgvector instalado: {pgvector}")
        return 0
    except Exception as e:  # noqa: BLE001
        print("ERRO:", type(e).__name__, str(e)[:300])
        return 3


if __name__ == "__main__":
    sys.exit(main())
