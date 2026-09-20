"""Os 60 enums de negócio do Radar Imobiliário, nomeados em português.

As contagens de valores **são contrato**: alterar qualquer uma delas é mudança de nível
`alto` ou `critico` por `R62.4`, e o meta-teste `MT-09` verifica uma a uma. Nenhum enum
recebe valor "por conveniência" — valor novo é decisão de negócio revisada.

A correspondência com os rótulos normativos escritos em inglês no requirements é a tabela
de correspondência do design (`D72`): o significado é o declarado lá e o identificador é o
declarado aqui, um para um. Sinônimo novo para termo já nomeado é defeito de redação, não
variação de estilo (`D103`).

Três enums são `IntEnum` porque a ordem é semântica e precisa ser comparável: `CamadaDeDecisao`
(a camada determinante é a de **menor** índice entre as eliminatórias, `R53.1`), `GateDeDados`
(`G0` a `G7`, `R4`), `NivelDeIdentidade` (`I0` a `I4`, `R7.1`) e `NivelDeReforma` (`0` a `4`,
`R29.1`). Os demais são `StrEnum`, porque o rótulo é o que se persiste e se audita.

Camada de núcleo: sem import externo, sem entrada e saída de dados.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum

__all__ = [
    "CamadaDeDecisao",
    "CategoriaDeDiferenca",
    "CategoriaDeLiquidez",
    "CategoriaDeRisco",
    "ClasseDeAtratividade",
    "ClasseDeComparavel",
    "ClasseDeConfiabilidadeDeFonte",
    "ClasseDeLocalizacao",
    "ClasseDeUrgencia",
    "EstadoDaCaptura",
    "EstadoDaInformacao",
    "EstadoDeAverbacaoDeLeilaoNegativo",
    "EstadoDeDecisao",
    "EstadoDeMonitoramento",
    "EstadoDeOcupacao",
    "EstadoDoImovel",
    "Estrategia",
    "FaseDeDiligencia",
    "FaseDoPipeline",
    "ForcaDeSinal",
    "FormatoNumerico",
    "GateDeDados",
    "GrupoDePerfil",
    "Impacto",
    "ImpactoDeProcesso",
    "Materialidade",
    "MetodoDeValuation",
    "Mitigacao",
    "NivelDeConfianca",
    "NivelDeIdentidade",
    "NivelDeReforma",
    "OrigemDeDocumento",
    "OrigemDeEvidencia",
    "PerfilDeAtivo",
    "PortaDeEntrada",
    "PotencialPreliminar",
    "PrioridadeDePendencia",
    "Probabilidade",
    "PublicoAlvo",
    "QualidadeDaEvidencia",
    "ResponsabilidadePeloDebito",
    "ResultadoDeEviccao",
    "ResultadoDeItemDeChecklist",
    "ResultadoDeTriagem",
    "ResultadoDeVerificacao",
    "ResultadoP0",
    "Robustez",
    "Severidade",
    "SituacaoDeDebito",
    "SituacaoDeGovernanca",
    "SituacaoDeProcesso",
    "SituacaoJuridica",
    "TipoDeArea",
    "TipoDeCenario",
    "TipoDeDebito",
    "TipoDeDocumento",
    "TipoDeRegra",
    "TipoDeSegmentoDeConhecimento",
    "UnidadeDePercentual",
    "VeredictoDeIdentidade",
]


# --------------------------------------------------------------------------------------
# Jornada macro e decisão
# --------------------------------------------------------------------------------------


class FaseDoPipeline(StrEnum):
    """As 16 fases persistidas da jornada macro (`R70.1`; `PipelinePhase` em `D72`).

    A ordem canônica de `R70.1` tem vinte etapas; estas dezesseis são os marcos persistidos,
    declarados na ordem em que ocorrem.
    """

    CAPTURADO = "CAPTURADO"
    NORMALIZADO = "NORMALIZADO"
    IDENTIFICADO = "IDENTIFICADO"
    DEDUPLICADO = "DEDUPLICADO"
    QUALIFICADO = "QUALIFICADO"
    CONSOLIDADO = "CONSOLIDADO"
    VALIDADO_JURIDICAMENTE = "VALIDADO_JURIDICAMENTE"
    ENRIQUECIDO = "ENRIQUECIDO"
    VALORADO = "VALORADO"
    CUSTEADO = "CUSTEADO"
    PONTUADO = "PONTUADO"
    RANQUEADO = "RANQUEADO"
    EM_ANALISE = "EM_ANALISE"
    DECIDIDO = "DECIDIDO"
    MONITORADO = "MONITORADO"
    ENCERRADO = "ENCERRADO"


class EstadoDeDecisao(StrEnum):
    """Os 6 vereditos possíveis (`R53.5`; `DecisionState` em `D72`).

    `BLOQUEAR` é o veredito jurídico e nada o supera (`SAFE-001`, `SAFE-002`);
    `PENDENTE_DE_DECISAO` é o estado da análise antes de `DECIDIDO`.
    """

    COMPRAR = "COMPRAR"
    COMPRAR_SE = "COMPRAR_SE"
    MONITORAR = "MONITORAR"
    NAO_COMPRAR = "NAO_COMPRAR"
    BLOQUEAR = "BLOQUEAR"
    PENDENTE_DE_DECISAO = "PENDENTE_DE_DECISAO"


class CamadaDeDecisao(IntEnum):
    """As 11 camadas de precedência, 0 a 10 (`R53.1`, `D.6.4`).

    `IntEnum` porque a camada determinante é a de **menor** índice entre as eliminatórias:
    a precedência tem de ser comparável. A decisão **não** é camada.
    """

    BLOQUEIOS_CRITICOS = 0
    VALIDADE_JURIDICA = 1
    ELEGIBILIDADE = 2
    DADOS_E_CONFIANCA = 3
    ECONOMIA = 4
    ESTRATEGIA = 5
    RISCO = 6
    LIQUIDEZ = 7
    ESCORE = 8
    CAPITAL_E_CONCENTRACAO = 9
    RANQUEAMENTO = 10


class Estrategia(StrEnum):
    """As 6 estratégias de investidor (`R44.1`). Estratégia não é perfil de ativo (`D.6.5`)."""

    REVENDA = "revenda"
    RENDA = "renda"
    VALORIZACAO = "valorizacao"
    MCMV = "mcmv"
    TERRENO = "terreno"
    CUSTOMIZADA = "customizada"


class PerfilDeAtivo(StrEnum):
    """Os 9 perfis de ativo (`R44.2`). `DESCONHECIDO` é perfil declarado, não ausência de campo."""

    APARTAMENTO = "apartamento"
    CASA_SOBRADO = "casa_sobrado"
    UM_DORMITORIO = "um_dormitorio"
    COMERCIAL = "comercial"
    GALPAO = "galpao"
    TERRENO = "terreno"
    RURAL = "rural"
    OUTROS = "outros"
    DESCONHECIDO = "desconhecido"


class ClasseDeUrgencia(StrEnum):
    """As 6 classes de urgência: `P0` a `P4` mais `BLOQUEAR` (`R52.6`)."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    BLOQUEAR = "BLOQUEAR"


class ClasseDeAtratividade(StrEnum):
    """As 5 classes de atratividade, `A1` a `A5` (`R52.6.1`, `SCORE-009`)."""

    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"


class TipoDeRegra(StrEnum):
    """Os 6 tipos de regra do catálogo canônico (`R54.1`)."""

    REGRA_DURA = "regra_dura"
    REGRA_BRANDA = "regra_branda"
    REGRA_CONDICIONAL = "regra_condicional"
    REGRA_INFORMATIVA = "regra_informativa"
    REGRA_DE_ESTRATEGIA = "regra_de_estrategia"
    REGRA_DE_EXCECAO = "regra_de_excecao"


# --------------------------------------------------------------------------------------
# Informação, evidência e confiança
# --------------------------------------------------------------------------------------


class EstadoDaInformacao(StrEnum):
    """Os 6 estados da informação (`R26.7`, `R56.5`).

    `DESCONHECIDO` é estado declarado e permanece `DESCONHECIDO` enquanto não houver nova
    evidência (`SAFE-003`, `SAFE-004`): nunca é substituído por zero nem por valor neutro.
    """

    OBSERVADO = "OBSERVADO"
    CONFIRMADO = "CONFIRMADO"
    CALCULADO = "CALCULADO"
    ESTIMADO = "ESTIMADO"
    INFERIDO = "INFERIDO"
    DESCONHECIDO = "DESCONHECIDO"


class QualidadeDaEvidencia(StrEnum):
    """Os 5 níveis de qualidade da prova (`R65.1.1`).

    `AUSENTE` é ausência de evidência — e ausência de evidência não é regularidade
    (`SAFE-017`).
    """

    FORTE = "forte"
    BOA = "boa"
    MODERADA = "moderada"
    FRACA = "fraca"
    AUSENTE = "ausente"


class OrigemDeEvidencia(StrEnum):
    """As 5 origens de evidência (`R89.2`)."""

    FONTE_OFICIAL = "FONTE_OFICIAL"
    DOCUMENTO = "DOCUMENTO"
    TERCEIRO = "TERCEIRO"
    USUARIO = "USUARIO"
    RADAR = "RADAR"


class NivelDeConfianca(StrEnum):
    """Os 6 níveis nomeados de confiança (`CONF-010`, `R50.5.1`).

    `INCONCLUSIVA` não é faixa numérica: é estado, e nenhum rótulo fora destes seis é válido.
    """

    MUITO_ALTA = "muito_alta"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"
    MUITO_BAIXA = "muito_baixa"
    INCONCLUSIVA = "inconclusiva"


class ClasseDeConfiabilidadeDeFonte(StrEnum):
    """As 6 classes de confiabilidade de fonte por categoria de dado (`R1.5`)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    U = "U"


class TipoDeSegmentoDeConhecimento(StrEnum):
    """Os 15 tipos de segmento da Base de Conhecimento (`R72.2`).

    `R72.2` enuncia "doze" e enumera quinze nomes; a enumeração prevalece, conforme o defeito
    de contagem registrado no design.
    """

    REGRA = "REGRA"
    DEFINICAO = "DEFINICAO"
    FORMULA = "FORMULA"
    CHECKLIST = "CHECKLIST"
    EVIDENCIA = "EVIDENCIA"
    CASO = "CASO"
    ANALISE = "ANALISE"
    MANUAL = "MANUAL"
    PARAMETRO = "PARAMETRO"
    EXCECAO = "EXCECAO"
    DECISAO = "DECISAO"
    GOVERNANCA = "GOVERNANCA"
    GUIA_DE_EVIDENCIA = "GUIA_DE_EVIDENCIA"
    ESTRATEGIA = "ESTRATEGIA"
    SEGURANCA = "SEGURANCA"


class SituacaoDeGovernanca(StrEnum):
    """As 6 situações de governança de artefato versionado (`R62.2`)."""

    RASCUNHO = "rascunho"
    EM_REVISAO = "em_revisao"
    APROVADO = "aprovado"
    ATIVO = "ativo"
    RETIRADO = "retirado"
    HISTORICO = "historico"


# --------------------------------------------------------------------------------------
# Jurídico e documental
# --------------------------------------------------------------------------------------


class SituacaoJuridica(StrEnum):
    """As 3 situações jurídicas (`R12.6`, `D.2.7`).

    Tipo fechado validado na fronteira: valor inesperado falha explicitamente, em lugar de
    seguir como se fosse `REGULAR`.
    """

    REGULAR = "REGULAR"
    PENDENTE = "PENDENTE"
    BLOQUEIO = "BLOQUEIO"


class ResultadoP0(StrEnum):
    """Os 5 resultados do gate jurídico `P0` (`R12.6`)."""

    REGULAR_COMPROVADO = "REGULAR_COMPROVADO"
    PENDENTE = "PENDENTE"
    RISCO_JURIDICO = "RISCO_JURIDICO"
    BLOQUEIO = "BLOQUEIO"
    INCONCLUSIVO = "INCONCLUSIVO"


class ResultadoDeVerificacao(StrEnum):
    """Os 5 resultados de uma verificação declarativa (`R20.4`, `REG-025`).

    `NAO_APLICAVEL` é distinto de `DESCONHECIDO` e de `IRREGULAR` (`D.2.8`, `SAFE-017`), e
    `EM_TRATAMENTO` é o estado próprio de `R13.13`.
    """

    CONFIRMADO = "CONFIRMADO"
    IRREGULAR = "IRREGULAR"
    DESCONHECIDO = "DESCONHECIDO"
    NAO_APLICAVEL = "NAO_APLICAVEL"
    EM_TRATAMENTO = "EM_TRATAMENTO"


class EstadoDeAverbacaoDeLeilaoNegativo(StrEnum):
    """Os 4 estados da averbação de leilão negativo (`R13.13`, `REG-003`)."""

    AVERBADO = "averbado"
    EM_TRATAMENTO = "em_tratamento"
    NAO_SE_APLICA = "nao_se_aplica"
    DESCONHECIDO = "desconhecido"


class ResultadoDeEviccao(StrEnum):
    """Os 3 resultados da verificação de cláusula de evicção (`R15.9`, `R15.9.1`).

    Cláusula comprovadamente ausente é `BLOQUEIO`; não verificada é `PENDENTE` — evidência de
    ausência e ausência de evidência não se confundem.
    """

    CLAUSULA_CONFIRMADA = "clausula_confirmada"
    CLAUSULA_AUSENTE_COMPROVADA = "clausula_ausente_comprovada"
    NAO_VERIFICADA = "nao_verificada"


class ImpactoDeProcesso(StrEnum):
    """Os 4 níveis de impacto de processo judicial (`R16.3`, `SAFE-014`).

    Só `MATERIAL_IMPEDITIVO` sem mitigação produz `BLOQUEAR`.
    """

    NENHUM = "nenhum"
    POTENCIAL = "potencial"
    MATERIAL_MITIGAVEL = "material_mitigavel"
    MATERIAL_IMPEDITIVO = "material_impeditivo"


class SituacaoDeProcesso(StrEnum):
    """As 5 situações de processo judicial (`R90.1`)."""

    EM_ANDAMENTO = "em_andamento"
    SUSPENSO = "suspenso"
    ARQUIVADO = "arquivado"
    EXTINTO = "extinto"
    DESCONHECIDA = "desconhecida"


class EstadoDeOcupacao(StrEnum):
    """Os 7 estados de ocupação (`R18.1`).

    Ocupação é risco, não nulidade (`SAFE-013`): vive na camada 6, exceto os dois casos de
    `BLOQUEAR` da camada 0 (`R18.2.1`, `R18.2.2`).
    """

    DESOCUPADO_CONFIRMADO = "desocupado_confirmado"
    LIVRE_NAO_CONFIRMADO = "livre_nao_confirmado"
    OCUPADO_PELO_DEVEDOR = "ocupado_pelo_devedor"
    OCUPADO_POR_TERCEIRO = "ocupado_por_terceiro"
    OCUPADO_POR_INQUILINO = "ocupado_por_inquilino"
    POSSE_LITIGIOSA = "posse_litigiosa"
    DESCONHECIDO = "desconhecido"


class TipoDeDocumento(StrEnum):
    """Os 9 tipos de documento (`R86.4`)."""

    MATRICULA = "MATRICULA"
    EDITAL = "EDITAL"
    IPTU = "IPTU"
    CONDOMINIO = "CONDOMINIO"
    PROCESSO_JUDICIAL = "PROCESSO_JUDICIAL"
    LAUDO = "LAUDO"
    FOTOS = "FOTOS"
    ORCAMENTO_REFORMA = "ORCAMENTO_REFORMA"
    OUTRO = "OUTRO"


class OrigemDeDocumento(StrEnum):
    """As 3 origens de documento (`R86.5`)."""

    CAPTURA_AUTOMATICA = "CAPTURA_AUTOMATICA"
    ENVIO_DO_USUARIO = "ENVIO_DO_USUARIO"
    PRODUCAO_INTERNA = "PRODUCAO_INTERNA"


class TipoDeDebito(StrEnum):
    """Os 4 tipos de débito (`R91.2`). Débito é entidade, não estimativa."""

    IPTU_E_TAXAS_MUNICIPAIS = "iptu_e_taxas_municipais"
    CONDOMINIO = "condominio"
    CONCESSIONARIAS = "concessionarias"
    DEMAIS_ENCARGOS = "demais_encargos"


class SituacaoDeDebito(StrEnum):
    """As 5 situações de débito (`R91.4`).

    Tipo exigido pelo checklist e não investigado permanece `DESCONHECIDO`, nunca zero
    (`R91.5`, `SAFE-005`).
    """

    EM_ABERTO = "em_aberto"
    PARCELADO = "parcelado"
    QUITADO = "quitado"
    EM_DISCUSSAO = "em_discussao"
    DESCONHECIDO = "desconhecido"


class ResponsabilidadePeloDebito(StrEnum):
    """As 3 responsabilidades atribuídas pelo edital (`R91.6`, `R91.7`)."""

    ADQUIRENTE = "adquirente"
    VENDEDOR = "vendedor"
    NAO_DECLARADA = "nao_declarada"


# --------------------------------------------------------------------------------------
# Captura, identidade, perfil e localização
# --------------------------------------------------------------------------------------


class EstadoDaCaptura(StrEnum):
    """Os 10 estados da captura (`CaptureState` em `D72`).

    `REJEITADA` é o estado do payload reprovado em `G0`: rejeição é resultado registrado, não
    oportunidade criada.
    """

    CAPTURADA = "CAPTURADA"
    NORMALIZADA = "NORMALIZADA"
    IDENTIFICADA = "IDENTIFICADA"
    VINCULADA = "VINCULADA"
    QUALIFICADA = "QUALIFICADA"
    ENRIQUECIDA = "ENRIQUECIDA"
    EXPIRADA = "EXPIRADA"
    SUBSTITUIDA = "SUBSTITUIDA"
    REJEITADA = "REJEITADA"
    ERRO = "ERRO"


class EstadoDoImovel(StrEnum):
    """Os 8 estados do imóvel (`PropertyState` em `D72`)."""

    CANDIDATO = "CANDIDATO"
    ATIVO = "ATIVO"
    EM_MONITORAMENTO = "EM_MONITORAMENTO"
    OPORTUNIDADE = "OPORTUNIDADE"
    ADQUIRIDO = "ADQUIRIDO"
    VENDIDO = "VENDIDO"
    INATIVO = "INATIVO"
    ENCERRADO = "ENCERRADO"


class GateDeDados(IntEnum):
    """Os 8 gates de dados, `G0` a `G7` (`R4.1` a `R4.8`).

    `IntEnum` porque os gates são atravessados em ordem crescente e a comparação é semântica.
    """

    G0 = 0
    G1 = 1
    G2 = 2
    G3 = 3
    G4 = 4
    G5 = 5
    G6 = 6
    G7 = 7


class PotencialPreliminar(StrEnum):
    """As 5 faixas de potencial preliminar (`R5.2`).

    A profundidade de investigação deriva daqui, nunca do `EscoreDeOportunidade` — derivar do
    escore criaria dependência circular.
    """

    DESCARTAVEL = "descartavel"
    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    EXCEPCIONAL = "excepcional"


class NivelDeIdentidade(IntEnum):
    """Os 5 níveis de identidade, `I0` a `I4` (`R7.1`).

    `IntEnum` porque nível mais alto é identidade mais forte, e a comparação é usada como
    pré-condição de etapas posteriores.
    """

    I0 = 0
    I1 = 1
    I2 = 2
    I3 = 3
    I4 = 4


class ForcaDeSinal(StrEnum):
    """As 6 forças de sinal de identificação (`R7.6`)."""

    DECISIVA = "decisiva"
    MUITO_FORTE = "muito_forte"
    FORTE = "forte"
    MEDIA = "media"
    FRACA = "fraca"
    BAIXA = "baixa"


class VeredictoDeIdentidade(StrEnum):
    """Os 3 vereditos de identidade (`R9.6`; `MatchVerdict` em `D72`)."""

    MESMO = "mesmo"
    DIFERENTE = "diferente"
    INDETERMINADO = "indeterminado"


class GrupoDePerfil(StrEnum):
    """Os 9 grupos do perfil do imóvel (`R10.8`)."""

    IDENTIFICACAO = "identificacao"
    LOCALIZACAO = "localizacao"
    FISICO = "fisico"
    CONDOMINIAL = "condominial"
    OCUPACIONAL = "ocupacional"
    QUALIDADE = "qualidade"
    OFERTA = "oferta"
    DOCUMENTAL = "documental"
    CONSOLIDACAO = "consolidacao"


class ClasseDeLocalizacao(StrEnum):
    """As 5 classes de localização, A a E (`R11.1`)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class PortaDeEntrada(StrEnum):
    """As 2 portas de entrada (`R84.1`).

    A porta é **proveniência**, nunca parâmetro de decisão (`R84.9`). Uma terceira porta não é
    configurável: é mudança de esquema com revisão de nível `critico`.
    """

    ANALISE_MANUAL = "ANALISE_MANUAL"
    RADAR_AUTOMATICO = "RADAR_AUTOMATICO"


class ResultadoDeTriagem(StrEnum):
    """Os 2 resultados da triagem rápida (`R93.3`).

    A triagem decide quem segue, nunca o que vale: não emite `EstadoDeDecisao` (`R93.2`).
    """

    CANDIDATO = "CANDIDATO"
    NAO_CANDIDATO = "NAO_CANDIDATO"


class CategoriaDeDiferenca(StrEnum):
    """As 5 categorias de diferença entre versões de análise (`R88.5`)."""

    NOVA_EVIDENCIA = "nova_evidencia"
    VALOR_ALTERADO = "valor_alterado"
    RISCO_ALTERADO = "risco_alterado"
    PENDENCIA_RESOLVIDA = "pendencia_resolvida"
    DECISAO_ALTERADA = "decisao_alterada"


# --------------------------------------------------------------------------------------
# Normalização numérica
# --------------------------------------------------------------------------------------


class FormatoNumerico(StrEnum):
    """Os 3 formatos numéricos aceitos na interpretação (`R3.4.1`, `R3.4.4`).

    `AUTO` decide por evidência estrutural, nunca por magnitude (`D.1.3`): ambiguidade resulta
    em `DESCONHECIDO`.
    """

    PT_BR = "pt_br"
    SIMPLES = "simples"
    AUTO = "auto"


class UnidadeDePercentual(StrEnum):
    """As 2 unidades de percentual (`R3.4.2`, `R3.4.3`).

    A unidade é obrigatória na entrada: sem ela, alíquota fracionária é interpretada errado
    (`D.1.4`).
    """

    FRACAO = "fracao"
    PORCENTO = "porcento"


# --------------------------------------------------------------------------------------
# Mercado, comparáveis e valuation
# --------------------------------------------------------------------------------------


class ClasseDeComparavel(StrEnum):
    """As 6 classes de comparável, A a E mais U (`CMP-014`)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    U = "U"


class TipoDeArea(StrEnum):
    """Os 5 tipos de área (`R3.5`, `R21.11`).

    Área de tipo desconhecido não é área privativa por omissão: o tipo é declarado.
    """

    PRIVATIVA = "privativa"
    COMUM = "comum"
    TOTAL = "total"
    TERRENO = "terreno"
    DESCONHECIDO = "DESCONHECIDO"


class MetodoDeValuation(StrEnum):
    """Os 7 métodos de valuation (`R24.2` a `R24.5`)."""

    COMPARATIVO = "comparativo"
    PRECO_M2_AJUSTADO = "preco_m2_ajustado"
    MESMO_CONDOMINIO = "mesmo_condominio"
    CAPITALIZACAO_DE_RENDA = "capitalizacao_de_renda"
    RESIDUAL_DE_POTENCIAL = "residual_de_potencial"
    ANALOGIA = "analogia"
    HIBRIDO = "hibrido"


class NivelDeReforma(IntEnum):
    """Os 5 níveis de reforma, 0 a 4 (`R29.1`).

    `IntEnum` porque o nível é ordinal e alimenta faixas de custo por metro quadrado.
    """

    N0 = 0
    N1 = 1
    N2 = 2
    N3 = 3
    N4 = 4


class TipoDeCenario(StrEnum):
    """Os 4 tipos de cenário (`R32.1`)."""

    OTIMISTA = "otimista"
    BASE = "base"
    CONSERVADOR = "conservador"
    ESTRESSADO = "estressado"


class Robustez(StrEnum):
    """Os 6 níveis de robustez do resultado entre cenários (`R32.6`)."""

    MUITO_ALTA = "muito_alta"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"
    ESPECULATIVA = "especulativa"
    INVIAVEL = "inviavel"


class CategoriaDeLiquidez(StrEnum):
    """As 7 faixas de liquidez (`R40.2`)."""

    MUITO_ALTA = "muito_alta"
    ALTA = "alta"
    BOA = "boa"
    MEDIA = "media"
    BAIXA = "baixa"
    MUITO_BAIXA = "muito_baixa"
    ILIQUIDA = "iliquida"


class PublicoAlvo(StrEnum):
    """Os 7 públicos-alvo de saída (`R40.9`)."""

    MORADOR = "morador"
    INVESTIDOR = "investidor"
    PRIMEIRO_IMOVEL = "primeiro_imovel"
    MCMV = "mcmv"
    ALTO_PADRAO = "alto_padrao"
    USUARIO_COMERCIAL = "usuario_comercial"
    COMPRADOR_DE_TERRENO = "comprador_de_terreno"


# --------------------------------------------------------------------------------------
# Risco, diligência, pendência e monitoramento
# --------------------------------------------------------------------------------------


class CategoriaDeRisco(StrEnum):
    """As 10 categorias de risco (`R34.1`)."""

    JURIDICO = "juridico"
    DOCUMENTAL = "documental"
    OCUPACAO = "ocupacao"
    FINANCEIRO = "financeiro"
    FISICO = "fisico"
    MERCADO = "mercado"
    LIQUIDEZ = "liquidez"
    OPERACIONAL = "operacional"
    ESTRATEGICO = "estrategico"
    INFORMACIONAL = "informacional"


class Probabilidade(StrEnum):
    """As 3 probabilidades da matriz de severidade (`R34.3`)."""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class Impacto(StrEnum):
    """Os 4 impactos da matriz de severidade (`R34.3`).

    Componente de custo `DESCONHECIDO` de impacto `ALTO` ou `CRITICO` marca o preço máximo como
    provisório (`R26.12`). Impacto não estimado é `Desconhecido`, nunca `BAIXO` por omissão.
    """

    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class Severidade(StrEnum):
    """As 4 severidades resultantes de probabilidade × impacto (`R34.4`)."""

    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class Mitigacao(StrEnum):
    """As 6 estratégias de mitigação de risco (`R34.10`)."""

    ELIMINAR = "eliminar"
    EVITAR = "evitar"
    REDUZIR = "reduzir"
    TRANSFERIR = "transferir"
    ACEITAR = "aceitar"
    CONDICIONAR = "condicionar"


class FaseDeDiligencia(StrEnum):
    """As 8 fases de due diligence, `DD-0` a `DD-7` (`R36.1`)."""

    DD0 = "DD-0"
    DD1 = "DD-1"
    DD2 = "DD-2"
    DD3 = "DD-3"
    DD4 = "DD-4"
    DD5 = "DD-5"
    DD6 = "DD-6"
    DD7 = "DD-7"


class ResultadoDeItemDeChecklist(StrEnum):
    """Os 6 resultados de item de checklist (`R36.3`; `ChecklistOutcome` em `D72`).

    `NAO_APLICAVEL` exige justificativa não nula (`R92.4`) e `DESCONHECIDO` não é favorável.
    """

    CONFIRMADO = "confirmado"
    PARCIALMENTE_CONFIRMADO = "parcialmente_confirmado"
    NAO_CONFIRMADO = "nao_confirmado"
    CONFLITANTE = "conflitante"
    NAO_APLICAVEL = "nao_aplicavel"
    DESCONHECIDO = "desconhecido"


class PrioridadeDePendencia(StrEnum):
    """As 4 prioridades de pendência (`R37.2`)."""

    CRITICA = "critica"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"


class EstadoDeMonitoramento(StrEnum):
    """Os 10 estados de monitoramento (`R57.10.1`)."""

    ATIVO = "ativo"
    AGUARDANDO_PRECO = "aguardando_preco"
    AGUARDANDO_EVIDENCIA = "aguardando_evidencia"
    AGUARDANDO_LIQUIDEZ = "aguardando_liquidez"
    AGUARDANDO_CONDICAO_DE_COMPRA = "aguardando_condicao_de_compra"
    AGUARDANDO_DECISAO_DO_INVESTIDOR = "aguardando_decisao_do_investidor"
    SUSPENSO_PELO_INVESTIDOR = "suspenso_pelo_investidor"
    REABERTO = "reaberto"
    ABANDONADO = "abandonado"
    ENCERRADO = "encerrado"


class Materialidade(StrEnum):
    """Os 5 níveis de materialidade de mudança monitorada (`R57.2`)."""

    CRITICO = "critico"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    INFORMATIVO = "informativo"
