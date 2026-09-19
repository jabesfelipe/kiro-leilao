"""Modelos ORM (SQLAlchemy 2.0) espelhando db/schema.sql.

Fonte de verdade do schema: spec/02_MODELO_DE_DADOS.md e db/schema.sql.
Enums reutilizam src/radar/domain/enums.py (uma única definição).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    Computed,
    Date,
    DateTime,
    FetchedValue,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from radar.domain.enums import (
    DecisionState,
    EvidenceState,
    PipelinePhase,
    Strategy,
)


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def _pg_enum(enum_cls: type, name: str) -> SAEnum:
    """Enum Postgres alinhado ao tipo criado em db/schema.sql.

    - StrEnum (Strategy, DecisionState, EvidenceState): persiste o .value.
    - IntEnum (PipelinePhase): o tipo SQL usa os NOMES das fases, então persiste
      o .name (comportamento padrão do SQLAlchemy).
    """
    first = next(iter(enum_cls))  # type: ignore[call-overload]
    if isinstance(first.value, str):
        return SAEnum(
            enum_cls,
            name=name,
            values_callable=lambda e: [m.value for m in e],
            create_type=False,
        )
    return SAEnum(enum_cls, name=name, create_type=False)


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[uuid.UUID] = _uuid_pk()
    source_type: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    reliability: Mapped[int | None] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Property(Base):
    __tablename__ = "properties"
    id: Mapped[uuid.UUID] = _uuid_pk()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    identifiers: Mapped[list["PropertyIdentifier"]] = relationship(back_populates="property")
    opportunities: Mapped[list["Opportunity"]] = relationship(back_populates="property")


class PropertyIdentifier(Base):
    __tablename__ = "property_identifiers"
    __table_args__ = (UniqueConstraint("property_id", "id_type", "value"),)
    id: Mapped[uuid.UUID] = _uuid_pk()
    property_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("properties.id", ondelete="CASCADE"))
    id_type: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[int | None] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    property: Mapped[Property] = relationship(back_populates="identifiers")


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[uuid.UUID] = _uuid_pk()
    source_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sources.id"))
    property_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("properties.id"))
    doc_type: Mapped[str] = mapped_column(Text, nullable=False)
    mime: Mapped[str | None] = mapped_column(Text)
    hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    uri: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (UniqueConstraint("document_id", "chunk_index"),)
    id: Mapped[uuid.UUID] = _uuid_pk()
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str | None] = mapped_column(Text)
    dominio: Mapped[str | None] = mapped_column(Text)
    topic: Mapped[str | None] = mapped_column(Text)
    rule_id: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[int | None] = mapped_column(SmallInteger)
    effective_from: Mapped[date | None] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
    confidence: Mapped[int | None] = mapped_column(SmallInteger)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    document: Mapped[Document] = relationship(back_populates="chunks")


class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[uuid.UUID] = _uuid_pk()
    property_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("properties.id", ondelete="CASCADE")
    )
    source_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sources.id"))
    external_ref: Mapped[str | None] = mapped_column(Text)
    auction_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    min_bid: Mapped[float | None] = mapped_column(Numeric(14, 2))
    current_phase: Mapped[PipelinePhase] = mapped_column(
        _pg_enum(PipelinePhase, "pipeline_phase"), default=PipelinePhase.CAPTURED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    property: Mapped[Property] = relationship(back_populates="opportunities")
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="opportunity")


class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (UniqueConstraint("opportunity_id", "version"),)
    id: Mapped[uuid.UUID] = _uuid_pk()
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE")
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    analysis_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    phase: Mapped[PipelinePhase] = mapped_column(
        _pg_enum(PipelinePhase, "pipeline_phase"), default=PipelinePhase.CAPTURED
    )
    identity_confidence: Mapped[int | None] = mapped_column(SmallInteger)
    legal_status: Mapped[str] = mapped_column(
        SAEnum("OK", "PENDENTE", "BLOCK", name="legal_status", create_type=False),
        default="PENDENTE",
    )
    occupancy_status: Mapped[str | None] = mapped_column(Text)
    market_value: Mapped[float | None] = mapped_column(Numeric(14, 2))
    economic_cost: Mapped[float | None] = mapped_column(Numeric(14, 2))
    net_discount: Mapped[float | None] = mapped_column(Numeric(6, 4))
    margin: Mapped[float | None] = mapped_column(Numeric(14, 2))
    liquidity_score: Mapped[int | None] = mapped_column(SmallInteger)
    strategy: Mapped[Strategy | None] = mapped_column(_pg_enum(Strategy, "strategy"))
    opportunity_score: Mapped[int | None] = mapped_column(SmallInteger)
    investor_fit: Mapped[int | None] = mapped_column(SmallInteger)
    confidence: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    decision: Mapped[DecisionState] = mapped_column(
        _pg_enum(DecisionState, "decision_state"), default=DecisionState.PENDING
    )
    explanation: Mapped[str | None] = mapped_column(Text)
    rule_version: Mapped[str] = mapped_column(Text, default="1.0.0")
    parameters_version: Mapped[str] = mapped_column(Text, default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    opportunity: Mapped[Opportunity] = relationship(back_populates="analyses")
    evidences: Mapped[list["EvidenceRow"]] = relationship(back_populates="analysis")


class EvidenceRow(Base):
    __tablename__ = "evidences"
    id: Mapped[uuid.UUID] = _uuid_pk()
    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyses.id", ondelete="CASCADE"))
    source_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sources.id"))
    document_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("documents.id"))
    location: Mapped[str | None] = mapped_column(Text)
    fact: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str | None] = mapped_column(Text)
    state: Mapped[EvidenceState] = mapped_column(_pg_enum(EvidenceState, "evidence_state"))
    confidence: Mapped[int | None] = mapped_column(SmallInteger)
    observed_at: Mapped[date | None] = mapped_column(Date)
    extracted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    rule_refs: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    analysis: Mapped[Analysis] = relationship(back_populates="evidences")


class Decision(Base):
    __tablename__ = "decisions"
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analyses.id", ondelete="CASCADE"), primary_key=True
    )
    decision: Mapped[DecisionState] = mapped_column(_pg_enum(DecisionState, "decision_state"))
    deciding_layer: Mapped[str] = mapped_column(Text, nullable=False)
    reasons: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Cost(Base):
    __tablename__ = "costs"
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analyses.id", ondelete="CASCADE"), primary_key=True
    )
    preco: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    comissao_leiloeiro: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    itbi: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    registro_documentacao: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    condominio_debitos: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    tributos_debitos: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    reforma: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    reserva_imprevistos: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    custo_juridico_esperado: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    carrying: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    # total é coluna GENERATED ALWAYS no banco: read-only, nunca no INSERT/UPDATE.
    total: Mapped[float | None] = mapped_column(
        Numeric(14, 2),
        Computed(
            "preco + comissao_leiloeiro + itbi + registro_documentacao "
            "+ condominio_debitos + tributos_debitos + reforma "
            "+ reserva_imprevistos + custo_juridico_esperado + carrying",
            persisted=True,
        ),
    )


# Constraint de exemplo espelhando o CHECK do schema
CheckConstraint("confidence BETWEEN 0 AND 100", name="ck_analysis_confidence")
