"""Smoke test do pgvector: grava chunks com embedding e faz busca por similaridade.

Prova que a camada de RAG (document_chunks + pgvector) está operacional.
Uso: python scripts/db_smoke_vector.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sqlalchemy import text

from radar.db.models import Document, DocumentChunk
from radar.db.session import get_session

DIM = 1536


def basis_embedding(axis: int, weight: float = 1.0) -> list[float]:
    """Vetor com direção distinta (peso num eixo), para o ranking ser significativo.

    Vetores constantes ([s]*DIM) seriam todos paralelos e a distância de cosseno
    daria ~0 para todos — inútil para testar ordenação.
    """
    v = [0.0] * DIM
    v[axis] = weight
    return v


def mixed_embedding(primary: int, secondary: int, ratio: float = 0.2) -> list[float]:
    """Vetor próximo de `primary`, com um componente menor em `secondary`."""
    v = [0.0] * DIM
    v[primary] = 1.0
    v[secondary] = ratio
    return v


def main() -> int:
    with get_session() as session:
        doc = Document(doc_type="edital", hash=f"smoke-vector-{id(object())}", uri="memoria://smoke")
        session.add(doc)
        session.flush()

        # cada chunk numa direção distinta (eixos 0, 1, 2)
        chunks = [
            ("Garantia contra evicção prevista no item 18.1 do edital.", 0),
            ("Consolidação da propriedade averbada em 31/07/2026.", 1),
            ("Comissão do leiloeiro de 5% sobre o valor da proposta.", 2),
        ]
        for i, (content, axis) in enumerate(chunks):
            session.add(
                DocumentChunk(
                    document_id=doc.id,
                    chunk_index=i,
                    content=content,
                    tipo="EVIDENCIA",
                    dominio="juridico",
                    embedding=basis_embedding(axis),
                )
            )
        doc_id = doc.id

    # consulta próxima do eixo 1 (consolidação) -> deve rankear esse chunk primeiro
    query = mixed_embedding(primary=1, secondary=0, ratio=0.2)
    with get_session() as session:
        rows = session.execute(
            text(
                "SELECT content, embedding <=> CAST(:q AS vector) AS distance "
                "FROM poc_ia.document_chunks "
                "WHERE document_id = :doc_id "
                "ORDER BY distance ASC LIMIT 3"
            ),
            {"q": str(query), "doc_id": str(doc_id)},
        ).all()

        print("=== busca por similaridade (pgvector) ===")
        for content, distance in rows:
            print(f"  {distance:.6f}  {content[:60]}")

        # o chunk mais próximo deve ser o da consolidação (eixo 1)
        top = rows[0][0]
        assert "Consolidação" in top, f"ranking inesperado; topo={top!r}"
        assert rows[0][1] < rows[1][1], "distâncias não estão ordenadas"
        print("ranking correto: consolidação em 1º (mais próxima da consulta).")

        total = session.execute(
            text("SELECT count(*) FROM poc_ia.document_chunks WHERE document_id = :d"),
            {"d": str(doc_id)},
        ).scalar_one()
        print(f"chunks gravados: {total}")

    # limpeza
    with get_session() as session:
        session.execute(
            text("DELETE FROM poc_ia.documents WHERE id = :d"), {"d": str(doc_id)}
        )
    print("limpeza concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
