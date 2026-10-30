# landed/app/main.py
# API Landed: custo de importação em BRL. Sem banco: as tabelas sintéticas ficam em código.
from decimal import Decimal
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import tabelas
from app.calculo import ErroCalculo, calcular

app = FastAPI(title="Landed — custo de importação", version="1.0.0")


class Entrada(BaseModel):
    ncm: str = Field(pattern=r"^\d{8}$")
    pais_origem: str = Field(default="", pattern=r"^([A-Z]{2})?$")  # informativo
    moeda: str = Field(pattern=r"^[A-Z]{3}$")
    valor_fob: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    frete: Decimal = Field(default=Decimal("0"), ge=0, max_digits=14, decimal_places=2)
    seguro: Decimal = Field(default=Decimal("0"), ge=0, max_digits=14, decimal_places=2)
    uf: str = Field(default="SP", pattern=r"^[A-Z]{2}$")
    modal: Literal["MARITIMO", "AEREO", "RODOVIARIO"] = "MARITIMO"


class Saida(BaseModel):
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
    aviso: str = "parâmetros sintéticos: não usar para fins fiscais"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ncm")
def listar_ncm() -> dict:
    """NCMs cobertos pela tabela sintética."""
    return {k: v.descricao for k, v in tabelas.NCM.items()}


@app.post("/calcular", response_model=Saida)
def post_calcular(e: Entrada) -> Saida:
    try:
        r = calcular(
            ncm=e.ncm, moeda=e.moeda, valor_fob=e.valor_fob, frete=e.frete,
            seguro=e.seguro, uf=e.uf, modal=e.modal,
        )
    except ErroCalculo as exc:
        raise HTTPException(422, str(exc)) from exc
    return Saida(**r.__dict__)
