"""Parsers tolerantes para formatos brasileiros. Retornam None quando não dá para
afirmar o valor — nunca inventam zero (regra: desconhecido ≠ zero)."""

from __future__ import annotations

import re
from datetime import date, datetime

_MONEY_RE = re.compile(r"-?[\d.]+(?:,\d+)?")


def parse_money(value: object) -> float | None:
    """'R$ 191.651,31' -> 191651.31 ; aceita float/int direto."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        return None
    m = _MONEY_RE.search(s.replace(" ", ""))
    if not m:
        return None
    num = m.group(0)
    # formato pt-BR: '.' milhar, ',' decimal
    num = num.replace(".", "").replace(",", ".")
    try:
        return float(num)
    except ValueError:
        return None


def parse_percent(value: object) -> float | None:
    """'5%' -> 0.05 ; '0,05' -> 0.05 ; 5 -> 0.05 ; 0.05 -> 0.05."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        return v / 100.0 if v > 1 else v
    s = str(value).strip()
    if not s:
        return None
    has_sign = "%" in s
    n = parse_money(s.replace("%", ""))
    if n is None:
        return None
    if has_sign or n > 1:
        return n / 100.0
    return n


def parse_area(value: object) -> float | None:
    """'47,76 m²' -> 47.76."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).lower().replace("m²", "").replace("m2", "").strip()
    return parse_money(s)


def parse_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else None


def parse_date(value: object) -> date | None:
    """'15/09/2026' ou '2026-09-15' -> date."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    s = str(value).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_datetime(value: object) -> datetime | None:
    """'15/09/2026 10:00' -> datetime; aceita só data (assume 00:00)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    s = str(value).strip()
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    d = parse_date(s)
    return datetime(d.year, d.month, d.day) if d else None


_OCCUPIED_HINTS = ("ocupado", "ocupada")
_VACANT_HINTS = ("desocupado", "desocupada", "livre", "vazio")


def parse_occupancy(value: object) -> bool | None:
    """Retorna True (ocupado), False (desocupado) ou None (não afirmável)."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if not s:
        return None
    # checa "desocupado" antes de "ocupado" (substring)
    if any(h in s for h in _VACANT_HINTS):
        return False
    if any(h in s for h in _OCCUPIED_HINTS):
        return True
    return None


def parse_bool(value: object) -> bool | None:
    """'sim'/'não'/'true'/'false' -> bool; desconhecido -> None."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in ("sim", "s", "true", "1", "yes", "y"):
        return True
    if s in ("nao", "não", "n", "false", "0", "no"):
        return False
    return None
