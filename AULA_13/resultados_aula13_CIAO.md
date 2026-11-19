# Aula 13 — Sprint 2 (AC-4): Operadores Evolucionários

Ambiente: Python 3 · pymoo 0.6.2 · numpy · matplotlib. Todos os scripts (`aula13_lab01.py` a `aula13_lab06.py`) executaram sem erros.

## a) Variáveis contínuas vs. inteiras

Rodando o problema do SOC (Exercício 1) **sem** operadores inteiros (NSGA-II padrão, `seed=42`), o algoritmo devolve soluções como:

| Pods | Analistas |
|---|---|
| 29.98 | 14.998 |
| 3.787 | 1.356 |
| 1.399 | 1.029 |

São configurações impossíveis na prática: não existe "1,4 pod" nem "1,36 analista". Arredondar depois da otimização pode quebrar a otimalidade ou gerar soluções duplicadas/dominadas.

Com `IntegerRandomSampling` + `SBX/PM(vtype=float, repair=RoundingRepair())` + `eliminate_duplicates=True`:

- A população inicial já nasce com valores inteiros dentro dos limites.
- SBX e PM continuam operando no espaço contínuo, mas o `RoundingRepair` arredonda cada filho **antes da avaliação**, então o algoritmo só "enxerga" soluções inteiras e viáveis.
- A fronteira de Pareto vira **discreta** (pontos em degraus, gráfico `aula13_lab01.png`), por exemplo: `30 pods / 15 analistas → 23,33 ms / R$ 1.215,00` e `4 pods / 1 analista → 250,00 ms / R$ 117,00`.
- `eliminate_duplicates=True` é importante: como muitos filhos arredondam para o mesmo par inteiro, sem ele a população se enche de cópias.

O mesmo vale para o Exercício 2 (Kubernetes): 25 soluções não dominadas, todas com réplicas e nodes inteiros (ex.: `20 réplicas / 6 nodes → 63,33 ms / US$ 750/mês`).

## b) Hipervolume — Exercício 4 (ponto de referência [400, 600], `pop_size=40`, `seed=42`)

| Configuração | Hipervolume |
|---|---|
| 10 gerações | **226.626,7048** |
| 80 gerações | **226.715,9378** |
| Ganho | +89,2330 (+0,039%) |

O HV aumentou com mais gerações, mostrando melhor convergência e distribuição da fronteira. O ganho relativo é pequeno porque o problema é bidimensional e simples (o NSGA-II já chega perto da fronteira em 10 gerações) e porque o ponto de referência está bem distante, o que torna a área total muito grande em relação ao refinamento obtido.

## c) Escala hospitalar recomendada — Exercício 6

Configuração: variáveis inteiras, restrição `g1 = f2_espera − 25 ≤ 0`, NSGA-II (`pop_size=40`, 50 gerações, `seed=42`), PseudoWeights `[0,40 custo; 0,60 espera]`. A fronteira final teve 40 soluções viáveis.

| Item | Valor |
|---|---|
| Médicos plantonistas | **17** |
| Enfermeiros | **32** |
| Custo do plantão | **R$ 34.800,00** |
| Tempo médio de espera | **18,09 min** |
| Restrição `f2_espera ≤ 25` | ✅ Atendida |
