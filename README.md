# Landed — custo de importação

API que calcula o **custo de importação (landed cost)** em reais: valor aduaneiro, II, IPI, PIS/COFINS-Importação, taxa Siscomex, AFRMM e ICMS "por dentro".
É o serviço de custo usado pelo [Rastreador de Importação](https://github.com/gabrielgmln-ops/Rastreador-de-Importacao).

**Parâmetros sintéticos:** alíquotas por NCM, câmbio e taxas fixas são fictícios. As fórmulas seguem a mecânica real; os números não servem para fins fiscais.

Stack: Python 3.12, FastAPI, pytest, Docker, GitHub Actions. Dinheiro sempre em `Decimal`.

## Subir

```bash
docker compose up --build -d     # http://localhost:8001/docs
```

## Contrato

`POST /calcular`

```json
{ "ncm": "84821010", "moeda": "USD", "valor_fob": "10000.00", "frete": "1500.00",
  "seguro": "120.50", "uf": "SP", "modal": "MARITIMO" }
```

`uf` (padrão SP) e `modal` (padrão MARITIMO) são opcionais. A resposta traz cada parcela e `custo_total`, todos como string com 2 casas.
NCM, moeda ou UF fora das tabelas → `422` com a mensagem. `GET /ncm` lista os NCMs cobertos.

## Fórmulas

1. Valor aduaneiro = (FOB + frete + seguro) × câmbio
2. II = VA × alíquota II
3. IPI = (VA + II) × alíquota IPI
4. PIS = VA × 2,10%; COFINS = VA × 9,65%
5. AFRMM = frete × câmbio × 8% (só marítimo); taxa Siscomex fixa
6. ICMS por dentro: base = (VA + II + IPI + PIS + COFINS + despesas) ÷ (1 − alíquota); ICMS = base × alíquota
7. Custo total = VA + tributos + despesas

## Prova

5 casos calculados à mão batem até o centavo: [docs/casos-a-mao.md](docs/casos-a-mao.md).

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m pytest     # cobertura mínima 95%
```
