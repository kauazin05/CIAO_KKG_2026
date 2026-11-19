
## Exercicio 1 - Compra de Servidores Cloud

**Objetivo:** Fronteira de Pareto simples com 2 objetivos opostos (Custo vs Latencia).

- Solucoes nao dominadas encontradas: 20
- Amostra de resultados:

| Custo (R$) | Latencia (ms) |
|---|---|
| 15.00 | 300.00 |
| 480.00 | 9.38 |
| 220.24 | 20.43 |
| 139.32 | 32.30 |
| 18.41 | 244.37 |

**Interpretacao:** quanto mais vCPUs alocadas, menor a latencia, porem maior o custo - confirma o trade-off esperado entre as duas pontas (barato/lento vs caro/rapido).

![Fronteira Exercicio 1](Imagens_Resultado/exercicio1_pareto.png)

---

## Exercicio 2 - Triagem de Incidentes SOC

**Objetivo:** completar a classe SOCAllocationProblem com os objetivos de custo e tempo de resposta.

**Formulas implementadas:**
- Custo: f1 = analistas * 100 + regimento * 50
- Tempo de resposta: f2 = 200 / analistas + 50 / regimento

- Solucoes nao dominadas encontradas: 30
- Amostra de resultados:

| Custo (R$) | Tempo (min) |
|---|---|
| 5499.11 | 9.00 |
| 151.60 | 247.16 |
| 289.01 | 127.40 |
| 394.28 | 102.68 |
| 830.47 | 51.00 |

**Interpretacao:** mais analistas e mais regimento de seguranca reduzem o tempo de resposta, mas aumentam o custo operacional proporcionalmente.

---

## Exercicio 3 - Logistica de Drones (3 Objetivos)

**Objetivo:** otimizacao com 3 objetivos simultaneos - Tempo, Custo e Pegada de Carbono (CO2).

- Solucoes nao dominadas encontradas: 40
- Amostra de resultados:

| Tempo (min) | Custo (R$) | CO2 |
|---|---|---|
| 12.5 | 702.02 | 96.74 |
| 100.0 | 258.32 | 3.02 |
| 100.0 | 60.0 | 15.0 |
| 68.62 | 71.24 | 21.86 |
| 79.33 | 93.3 | 12.21 |

**Interpretacao:** maior velocidade reduz o tempo de entrega, mas aumenta custo e emissao de CO2 simultaneamente - fronteira tridimensional confirmando o trade-off entre as 3 dimensoes.

![Fronteira Exercicio 3](Imagens_Resultado/exercicio3_pareto3d.png)

---

## Exercicio 4 - Selecao de Portfolio de Investimentos

**Objetivo:** completar objetivos de Risco vs Retorno, com inversao de sinal para maximizacao.

**Formulas implementadas:**
- Retorno (maximizar via sinal invertido): f1 = -(rf * 0.08 + acoes * 0.18)
- Risco (minimizar): f2 = rf * 0.02 + acoes * 0.25

- Solucoes nao dominadas encontradas: 30
- Amostra de resultados (sinal do retorno revertido para interpretacao):

| Risco | Retorno (%) |
|---|---|
| 0.0 | 0.01 |
| 27.0 | 26.0 |
| 7.42 | 11.47 |
| 14.4 | 16.92 |
| 9.33 | 13.27 |

**Interpretacao:** alocar mais em renda fixa reduz risco e retorno; alocar mais em acoes aumenta ambos. Fronteira de Pareto classica do dilema risco/retorno.

![Fronteira Exercicio 4](Imagens_Resultado/exercicio4_pareto.png)

---

## Exercicio 5 - Trade-off de Modelos de Machine Learning

**Objetivo:** escolha de hiperparametros (profundidade da arvore, numero de estimadores) minimizando Erro e Latencia.

- Solucoes nao dominadas encontradas: 30
- Amostra de resultados:

| Erro | Latencia (ms) |
|---|---|
| 0.4963 | 5.2 |
| 0.0072 | 105.95 |
| 0.2374 | 5.42 |
| 0.0109 | 22.75 |
| 0.0086 | 49.2 |

**Interpretacao:** modelos mais profundos/com mais estimadores reduzem o erro de predicao, mas aumentam o tempo de inferencia - trade-off classico entre precisao e complexidade computacional.

![Fronteira Exercicio 5](Imagens_Resultado/exercicio5_pareto.png)

---

## Exercicio 6 - Desafio Integrado com Restricoes (EV Battery)

**Objetivo:** aplicar restricao de desigualdade G(x) <= 0 em problema de recarga de veiculo eletrico.

**Implementacao:**
- n_ieq_constr=1 configurado no construtor
- Restricao: g1 = desgaste_bateria - 1500.0 (satisfeita quando desgaste <= 1500)
- out["G"] = [g1] entregue ao solver

- Total de solucoes retornadas: 40
- Solucoes viaveis (desgaste <= 1500): 40 (100%)
- Amostra de resultados viaveis:

| Tempo Recarga (min) | Desgaste |
|---|---|
| 20.0 | 1377.84 |
| 300.0 | 23.72 |
| 30.64 | 726.61 |
| 73.06 | 197.36 |
| 211.72 | 40.1 |

**Interpretacao:** recarga rapida (alta potencia) aproxima o desgaste do limite de seguranca (1500); recarga lenta preserva a bateria. Todas as solucoes encontradas respeitaram a restricao.

![Fronteira Exercicio 6](Imagens_Resultado/exercicio6_pareto.png)

---

## Exercicio 7 - Dimensionamento de Frota de Robos de Logistica (do zero)

**Objetivo:** modelar e implementar do zero a classe FrotaRobosProblem, sem esqueleto fornecido.

**Modelagem:**
- Variaveis: x1 = numero de robos [5, 50], x2 = velocidade [1.0, 4.0] m/s
- Objetivo 1 (custo, mil R$): f1 = x1*25.0 + x2^2*8.0
- Objetivo 2 (tempo de ciclo, min): f2 = 120.0/x1 + 40.0/x2
- Restricao (consumo energetico): g1 = x1*x2^1.5 - 120.0 <= 0
- Algoritmo: NSGA-II, populacao de 40, 60 geracoes

**Solucoes nao dominadas encontradas: 40**

**3 solucoes de trade-off selecionadas:**

| Solucao | N Robos | Velocidade (m/s) | Custo (mil R$) | Tempo de Ciclo (min) |
|---|---|---|---|---|
| A - Menor Custo | 5.0 | 1.0 | 133.01 | 63.97 |
| C - Intermediaria | 7.47 | 2.85 | 251.71 | 30.1 |
| B - Menor Tempo | 15.44 | 3.92 | 509.12 | 17.97 |

**Interpretacao:** a Solucao A favorece investimento minimo, mas com operacao lenta; a Solucao B exige investimento alto em frota e velocidade para maximizar a eficiencia operacional; a Solucao C representa um equilibrio pratico entre os dois extremos. A empresa escolheria conforme sua prioridade orcamentaria versus necessidade de giro operacional.

![Fronteira Exercicio 7](Imagens_Resultado/exercicio7_pareto.png)

---

## Conclusao Geral

Os 7 exercicios demonstraram, em cenarios de negocio distintos (cloud computing, seguranca, logistica de drones, investimentos, machine learning, veiculos eletricos e robotica), o mesmo principio central da otimizacao multiobjetivo: nao existe uma unica solucao otima quando os objetivos competem entre si, mas sim um conjunto de alternativas eficientes (Fronteira de Pareto) que cabe ao tomador de decisao escolher conforme suas prioridades de negocio. O algoritmo NSGA-II, via pymoo, mostrou-se consistente na geracao dessas fronteiras, inclusive em cenarios com restricoes de desigualdade (Exercicios 6 e 7) e com 3 objetivos simultaneos (Exercicio 3).
