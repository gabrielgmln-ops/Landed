# landed/tests/test_api.py
# Contrato HTTP consumido pelo Rastreador de Importação.
from fastapi.testclient import TestClient

from app.main import app

c = TestClient(app)

CORPO = {
    "ncm": "84821010",
    "pais_origem": "CN",
    "moeda": "USD",
    "valor_fob": "10000.00",
    "frete": "1500.00",
    "seguro": "120.50",
}


def test_health():
    assert c.get("/health").json() == {"status": "ok"}


def test_calcular_contrato_do_rastreador():
    r = c.post("/calcular", json=CORPO)
    assert r.status_code == 200
    corpo = r.json()
    # Dinheiro sai como string: nenhum consumidor recebe float
    assert corpo["custo_total"] == "101570.76"
    assert corpo["icms"] == "18282.74"
    assert "sintéticos" in corpo["aviso"]


def test_uf_e_modal_opcionais_mudam_o_resultado():
    aereo_rj = c.post("/calcular", json=CORPO | {"uf": "RJ", "modal": "AEREO"}).json()
    assert aereo_rj["afrmm"] == "0.00"
    assert aereo_rj["custo_total"] != "101570.76"


def test_ncm_fora_da_tabela_422_com_mensagem():
    r = c.post("/calcular", json=CORPO | {"ncm": "99999999"})
    assert r.status_code == 422
    assert "NCM 99999999" in r.json()["detail"]


def test_validacao_de_entrada():
    assert c.post("/calcular", json=CORPO | {"valor_fob": "-1"}).status_code == 422
    assert c.post("/calcular", json=CORPO | {"valor_fob": "1.001"}).status_code == 422
    assert c.post("/calcular", json=CORPO | {"ncm": "123"}).status_code == 422
    assert c.post("/calcular", json=CORPO | {"modal": "FERROVIARIO"}).status_code == 422


def test_lista_ncm():
    assert "84821010" in c.get("/ncm").json()
