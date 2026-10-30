# Casos calculados à mão

Parâmetros sintéticos (`app/tabelas.py`). Cada parcela é arredondada a 2 casas (meio para cima) antes do passo seguinte.

## Caso 1 — rolamentos, USD, SP, marítimo

NCM 84821010 (II 14%, IPI 5%), FOB 10.000,00, frete 1.500,00, seguro 120,50, câmbio 5,40, ICMS SP 18%.

| Passo | Conta | Resultado |
|---|---|---|
| Valor aduaneiro | (10.000,00 + 1.500,00 + 120,50) × 5,40 = 11.620,50 × 5,40 | 62.750,70 |
| II | 62.750,70 × 14% = 8.785,098 | 8.785,10 |
| IPI | (62.750,70 + 8.785,10) × 5% = 71.535,80 × 5% | 3.576,79 |
| PIS | 62.750,70 × 2,10% = 1.317,7647 | 1.317,76 |
| COFINS | 62.750,70 × 9,65% = 6.055,44255 | 6.055,44 |
| Taxa Siscomex | fixa | 154,23 |
| AFRMM | 1.500,00 × 5,40 × 8% | 648,00 |
| Soma antes do ICMS | 62.750,70 + 8.785,10 + 3.576,79 + 1.317,76 + 6.055,44 + 154,23 + 648,00 | 83.288,02 |
| Base do ICMS (por dentro) | 83.288,02 ÷ (1 − 0,18) = 101.570,756 | 101.570,76 |
| ICMS | 101.570,76 × 18% = 18.282,7368 | 18.282,74 |
| **Custo total** | 83.288,02 + 18.282,74 | **101.570,76** |

Com o ICMS por dentro, o custo total coincide com a base do ICMS: é a prova de que o imposto foi incluído na própria base.

## Casos 2 a 5 (resumo)

| Caso | Entrada | VA | II | IPI | PIS | COFINS | AFRMM | ICMS | Total |
|---|---|---|---|---|---|---|---|---|---|
| 2 | NCM 85414300, EUR 20.000 + frete 2.000, RJ 20%, aéreo | 128.700,00 | 15.444,00 | 0,00 | 2.702,70 | 12.419,55 | 0,00 | 39.855,12 | 199.275,60 |
| 3 | NCM 85423190, CNY 100.000 + 5.000 + 300, SC 17%, marítimo | 78.975,00 | 0,00 | 0,00 | 1.658,48 | 7.621,09 | 300,00 | 18.169,27 | 106.878,07 |
| 4 | NCM 87089990, USD 1.234,56 + 98,76 + 12,34, MG 18%, rodoviário | 7.266,56 | 1.307,98 | 278,67 | 152,60 | 701,22 | 0,00 | 2.164,67 | 12.025,93 |
| 5 | NCM 52081200, BRL 50.000, sem frete, SP 18%, marítimo | 50.000,00 | 13.000,00 | 0,00 | 1.050,00 | 4.825,00 | 0,00 | 15.152,76 | 84.181,99 |

Detalhes que os casos exercitam: arredondamento de .475 para .48 (caso 3), valor aduaneiro com três casas (caso 4), AFRMM zerado fora do marítimo (2 e 4) e sem frete (5).
Todos estão em `tests/test_calculo.py`.
