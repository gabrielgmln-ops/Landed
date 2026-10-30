# landed/tests/test_calculo.py
# Cinco casos calculados à mão (passo a passo em docs/casos-a-mao.md), batendo até o centavo.
from decimal import Decimal as D

import pytest

from app.calculo import ErroCalculo, calcular

CASOS = [
    # 1. Rolamentos, USD, SP, marítimo (II 14%, IPI 5%)
    (
        dict(ncm="84821010", moeda="USD", valor_fob=D("10000.00"), frete=D("1500.00"),
             seguro=D("120.50"), uf="SP", modal="MARITIMO"),
        dict(valor_aduaneiro="62750.70", ii="8785.10", ipi="3576.79", pis="1317.76",
             cofins="6055.44", afrmm="648.00", base_icms="101570.76", icms="18282.74",
             custo_total="101570.76"),
    ),
    # 2. Painéis solares, EUR, RJ (ICMS 20%), aéreo: sem AFRMM, IPI zero
    (
        dict(ncm="85414300", moeda="EUR", valor_fob=D("20000.00"), frete=D("2000.00"),
             seguro=D("0"), uf="RJ", modal="AEREO"),
        dict(valor_aduaneiro="128700.00", ii="15444.00", ipi="0.00", pis="2702.70",
             cofins="12419.55", afrmm="0.00", base_icms="199275.60", icms="39855.12",
             custo_total="199275.60"),
    ),
    # 3. Circuitos integrados, CNY, SC (17%): II e IPI zero; PIS arredonda .475 → .48
    (
        dict(ncm="85423190", moeda="CNY", valor_fob=D("100000.00"), frete=D("5000.00"),
             seguro=D("300.00"), uf="SC", modal="MARITIMO"),
        dict(valor_aduaneiro="78975.00", ii="0.00", ipi="0.00", pis="1658.48",
             cofins="7621.09", afrmm="300.00", base_icms="106878.07", icms="18169.27",
             custo_total="106878.07"),
    ),
    # 4. Autopeças, valores quebrados, MG, rodoviário: VA arredonda 7266.564 → 7266.56
    (
        dict(ncm="87089990", moeda="USD", valor_fob=D("1234.56"), frete=D("98.76"),
             seguro=D("12.34"), uf="MG", modal="RODOVIARIO"),
        dict(valor_aduaneiro="7266.56", ii="1307.98", ipi="278.67", pis="152.60",
             cofins="701.22", afrmm="0.00", base_icms="12025.93", icms="2164.67",
             custo_total="12025.93"),
    ),
    # 5. Tecido em BRL, marítimo sem frete: AFRMM zero mesmo no marítimo
    (
        dict(ncm="52081200", moeda="BRL", valor_fob=D("50000.00"), frete=D("0"),
             seguro=D("0"), uf="SP", modal="MARITIMO"),
        dict(valor_aduaneiro="50000.00", ii="13000.00", ipi="0.00", pis="1050.00",
             cofins="4825.00", afrmm="0.00", base_icms="84181.99", icms="15152.76",
             custo_total="84181.99"),
    ),
]


@pytest.mark.parametrize("entrada,esperado", CASOS, ids=[f"caso{i}" for i in range(1, 6)])
def test_casos_calculados_a_mao(entrada, esperado):
    r = calcular(**entrada)
    for campo, valor in esperado.items():
        assert getattr(r, campo) == D(valor), campo
    assert r.taxa_siscomex == D("154.23")


def test_total_e_soma_das_parcelas():
    r = calcular(**CASOS[0][0])
    assert r.custo_total == (
        r.valor_aduaneiro + r.ii + r.ipi + r.pis + r.cofins + r.icms + r.taxa_siscomex + r.afrmm
    )
    assert r.tributos == r.ii + r.ipi + r.pis + r.cofins + r.icms


def test_resultado_sempre_com_duas_casas():
    r = calcular(**CASOS[3][0])
    for v in r.__dict__.values():
        if v is not r.cambio:
            assert v.as_tuple().exponent == -2


@pytest.mark.parametrize(
    "mudanca,mensagem",
    [({"ncm": "99999999"}, "NCM"), ({"moeda": "JPY"}, "moeda"), ({"uf": "AM"}, "UF")],
)
def test_entradas_fora_da_tabela(mudanca, mensagem):
    with pytest.raises(ErroCalculo, match=mensagem):
        calcular(**(CASOS[0][0] | mudanca))
