"""Normalizador de ofertas da CAIXA (fonte inicial do MVP).

Recebe o payload cru capturado (dict com rótulos como aparecem na fonte) e produz
um NormalizedListing. Tolerante a variações de rótulo; o que não der para afirmar
fica None (UNKNOWN).

A captura em si (scraping/Download do edital) é responsabilidade de um coletor
externo — este módulo não inventa dado nem assume valor default.
"""

from __future__ import annotations

from typing import Any

from radar.capture.parsing import (
    parse_area,
    parse_bool,
    parse_datetime,
    parse_date,
    parse_int,
    parse_money,
    parse_occupancy,
    parse_percent,
)
from radar.capture.schemas import NormalizedListing, RawCapture

# rótulos aceitos por campo (primeiro encontrado vence)
FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "source_ref": ("numero_imovel", "número do imóvel", "id_imovel", "codigo", "source_ref"),
    "matricula": ("matricula", "matrícula", "matricula_numero"),
    "comarca": ("comarca",),
    "cartorio": ("cartorio", "cartório", "oficio", "ofício"),
    "endereco": ("endereco", "endereço", "localizacao", "localização"),
    "cidade": ("cidade", "municipio", "município"),
    "uf": ("uf", "estado"),
    "bairro": ("bairro",),
    "cep": ("cep",),
    "tipo_imovel": ("tipo_imovel", "tipo de imóvel", "tipo", "descricao_tipo"),
    "area_m2": ("area_privativa", "área privativa", "area_total", "área total", "area", "área"),
    "quartos": ("quartos", "dormitorios", "dormitórios"),
    "vagas": ("vagas", "garagem", "vagas_garagem"),
    "edital": ("edital", "numero_edital", "número do edital"),
    "item": ("item", "numero_item", "lote"),
    "modalidade": ("modalidade", "modalidade_venda", "tipo_venda"),
    "auction_date": (
        "data_leilao",
        "data do leilão",
        "data_sessao",
        "data da sessão",
        "data_hora",
    ),
    "min_bid": (
        "valor_minimo",
        "valor mínimo",
        "lance_minimo",
        "lance mínimo",
        "valor_venda",
        "preco",
        "preço",
    ),
    "avaliacao_fonte": ("valor_avaliacao", "valor de avaliação", "avaliacao", "avaliação"),
    "comissao_leiloeiro_pct": ("comissao_leiloeiro", "comissão do leiloeiro", "comissao"),
    "forma_pagamento": ("forma_pagamento", "formas de pagamento", "condicoes_pagamento"),
    "leiloeiro": ("leiloeiro", "nome_leiloeiro"),
    "situacao_texto": ("situacao", "situação", "situacao_ocupacao"),
    "consolidacao_data": ("data_consolidacao", "consolidacao_data"),
    "observed_at": ("data_consulta", "observed_at", "data_captura"),
}


def _norm_key(k: str) -> str:
    return k.strip().lower().replace("_", " ")


def _lookup(payload: dict[str, Any], aliases: tuple[str, ...]) -> Any:
    """Busca o primeiro alias presente, comparando chaves normalizadas."""
    index = {_norm_key(k): v for k, v in payload.items()}
    for alias in aliases:
        v = index.get(_norm_key(alias))
        if v is not None and str(v).strip() != "":
            return v
    return None


def normalize_caixa(capture: RawCapture) -> NormalizedListing:
    """Converte um payload cru da Caixa em NormalizedListing."""
    p = capture.payload

    def g(field: str) -> Any:
        return _lookup(p, FIELD_ALIASES.get(field, (field,)))

    ocupado = parse_occupancy(g("situacao_texto"))
    if ocupado is None:
        ocupado = parse_occupancy(_lookup(p, ("ocupado", "ocupacao", "ocupação")))

    return NormalizedListing(
        source_ref=_as_str(g("source_ref")),
        matricula=_as_str(g("matricula")),
        comarca=_as_str(g("comarca")),
        cartorio=_as_str(g("cartorio")),
        endereco=_as_str(g("endereco")),
        cidade=_as_str(g("cidade")),
        uf=_as_str(g("uf")),
        bairro=_as_str(g("bairro")),
        cep=_as_str(g("cep")),
        tipo_imovel=_as_str(g("tipo_imovel")),
        area_m2=parse_area(g("area_m2")),
        quartos=parse_int(g("quartos")),
        vagas=parse_int(g("vagas")),
        edital=_as_str(g("edital")),
        item=_as_str(g("item")),
        modalidade=_as_str(g("modalidade")),
        auction_date=parse_datetime(g("auction_date")),
        min_bid=parse_money(g("min_bid")),
        avaliacao_fonte=parse_money(g("avaliacao_fonte")),
        comissao_leiloeiro_pct=parse_percent(g("comissao_leiloeiro_pct")),
        forma_pagamento=_as_str(g("forma_pagamento")),
        leiloeiro=_as_str(g("leiloeiro")),
        ocupado=ocupado,
        situacao_texto=_as_str(g("situacao_texto")),
        consolidacao_averbada=parse_bool(
            _lookup(p, ("consolidacao_averbada", "consolidação averbada", "consolidacao"))
        ),
        consolidacao_data=parse_date(g("consolidacao_data")),
        leiloes_negativos_averbados=parse_bool(
            _lookup(p, ("leiloes_negativos_averbados", "averbacao_leiloes_negativos"))
        ),
        observed_at=parse_date(g("observed_at")) or capture.captured_at.date(),
        links=_as_links(_lookup(p, ("link", "links", "url"))),
    )


def _as_str(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def _as_links(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []
