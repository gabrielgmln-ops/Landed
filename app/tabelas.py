# landed/app/tabelas.py
# Parâmetros do cálculo. TODOS SINTÉTICOS: alíquotas por NCM, câmbio e valores fixos
# servem para demonstrar a mecânica, não para cálculo fiscal real.
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Aliquotas:
    descricao: str
    ii: Decimal
    ipi: Decimal
    pis: Decimal = Decimal("0.0210")      # PIS-Importação, regime geral
    cofins: Decimal = Decimal("0.0965")   # COFINS-Importação, regime geral


# Tabela sintética de NCMs (cobre os processos de demonstração do Rastreador)
NCM: dict[str, Aliquotas] = {
    "84821010": Aliquotas("Rolamentos de esferas", Decimal("0.14"), Decimal("0.05")),
    "85414300": Aliquotas("Módulos fotovoltaicos", Decimal("0.12"), Decimal("0.00")),
    "52081200": Aliquotas("Tecido de algodão", Decimal("0.26"), Decimal("0.00")),
    "85423190": Aliquotas("Circuitos integrados", Decimal("0.00"), Decimal("0.00")),
    "84224090": Aliquotas("Máquinas de embalagem", Decimal("0.14"), Decimal("0.0325")),
    "87089990": Aliquotas("Partes de veículos", Decimal("0.18"), Decimal("0.0325")),
}

# Câmbio sintético (BRL por unidade da moeda estrangeira)
CAMBIO: dict[str, Decimal] = {
    "USD": Decimal("5.4000"),
    "EUR": Decimal("5.8500"),
    "CNY": Decimal("0.7500"),
    "BRL": Decimal("1"),
}

# ICMS sintético por UF de destino
ICMS: dict[str, Decimal] = {
    "SP": Decimal("0.18"),
    "RJ": Decimal("0.20"),
    "MG": Decimal("0.18"),
    "SC": Decimal("0.17"),
}

TAXA_SISCOMEX = Decimal("154.23")   # valor fixo sintético por declaração
AFRMM = Decimal("0.08")             # sobre o frete, só no modal marítimo
