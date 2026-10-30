# landed/app/calculo.py
# Cálculo do custo de importação (landed cost) em BRL, passo a passo.
# Cada tributo é arredondado a 2 casas (HALF_UP) antes de entrar no passo seguinte,
# como numa declaração de importação: o total é a soma de valores já arredondados.
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from app import tabelas

CENTAVO = Decimal("0.01")


class ErroCalculo(ValueError):
    """Entrada fora do que a tabela sintética cobre (NCM, moeda ou UF desconhecidos)."""


def r2(v: Decimal) -> Decimal:
    return v.quantize(CENTAVO, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Resultado:
    cambio: Decimal
    valor_aduaneiro: Decimal
    ii: Decimal
    ipi: Decimal
    pis: Decimal
    cofins: Decimal
    taxa_siscomex: Decimal
    afrmm: Decimal
    base_icms: Decimal
    icms: Decimal
    tributos: Decimal
    custo_total: Decimal


def calcular(
    *,
    ncm: str,
    moeda: str,
    valor_fob: Decimal,
    frete: Decimal,
    seguro: Decimal,
    uf: str = "SP",
    modal: str = "MARITIMO",
) -> Resultado:
    try:
        aliq = tabelas.NCM[ncm]
    except KeyError:
        raise ErroCalculo(f"NCM {ncm} fora da tabela sintética") from None
    if moeda not in tabelas.CAMBIO:
        raise ErroCalculo(f"moeda {moeda} sem câmbio cadastrado")
    if uf not in tabelas.ICMS:
        raise ErroCalculo(f"UF {uf} sem alíquota de ICMS cadastrada")
    cambio = tabelas.CAMBIO[moeda]

    # 1. Valor aduaneiro (CIF) em reais
    va = r2((valor_fob + frete + seguro) * cambio)

    # 2. Tributos federais
    ii = r2(va * aliq.ii)
    ipi = r2((va + ii) * aliq.ipi)          # IPI incide sobre VA + II
    pis = r2(va * aliq.pis)                 # PIS/COFINS-Importação: base = VA
    cofins = r2(va * aliq.cofins)

    # 3. Despesas aduaneiras
    siscomex = tabelas.TAXA_SISCOMEX
    afrmm = r2(frete * cambio * tabelas.AFRMM) if modal == "MARITIMO" else Decimal("0.00")

    # 4. ICMS "por dentro": o imposto integra a própria base
    aliq_icms = tabelas.ICMS[uf]
    soma = va + ii + ipi + pis + cofins + siscomex + afrmm
    base_icms = r2(soma / (1 - aliq_icms))
    icms = r2(base_icms * aliq_icms)

    tributos = ii + ipi + pis + cofins + icms
    total = va + tributos + siscomex + afrmm
    return Resultado(
        cambio=cambio, valor_aduaneiro=va, ii=ii, ipi=ipi, pis=pis, cofins=cofins,
        taxa_siscomex=siscomex, afrmm=afrmm, base_icms=base_icms, icms=icms,
        tributos=tributos, custo_total=total,
    )
