"""Engine e sessão SQLAlchemy."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from radar.config import settings

engine = create_engine(
    settings.sqlalchemy_url(),
    future=True,
    pool_pre_ping=True,
    connect_args={"options": f"-csearch_path={settings.db_schema},public"},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
