# AULA 08 — Fechamento da AC-2
Otimização de Sistemas Computacionais e Resiliência de Redes

Artefatos: `lab01_aula08.py`, `lab02_aula08.py`, `lab03_aula08.py` (todos executados; gráficos em `.png`).

> **Premissas.** O roteiro não fornece alguns dados numéricos (modelo térmico do Lab 01, tabela de microsserviços do Lab 02, matriz D e pares críticos do Lab 03). Eles foram definidos nos próprios scripts, com semente fixa, e estão descritos abaixo. Se o professor passar os dados oficiais, basta trocar as constantes no topo de cada arquivo.

---

## Lab 01 — PSO para balanceamento de carga em datacenter

**Modelo.** Temperatura da AZ *i*: `T_i = C_i + 40·w_i`, com C = [42, 35, 58, 30, 50, 65] °C.
Fitness (minimizar): `f(W) = Σ w_i·T_i + 1000·Σ max(0, T_i − 75)²`.

**PSO.** Inércia 0,72; c1 = c2 = 1,49; 150 iterações; velocidade limitada a ±0,3. A cada iteração as posições passam pelo operador de normalização (`w ← max(w,0)`, `w ← w / Σw`), garantindo Σwᵢ = 1. Sementes fixas (42) para a tabela; 30 sementes para a robustez.

| População | W* = [w1 … w6] | Σwᵢ | T máx (°C) | Fitness |
|---|---|---|---|---|
| 10 | [0,2406, 0,3281, 0,0406, 0,3906, 0,0000, 0,0000] | 1,0000 | 65,0 | 48,4578 |
| 30 | [0,2125, 0,3000, 0,0125, 0,3625, 0,1125, 0,0000] | 1,0000 | 65,0 | 47,8250 |
| 50 | [0,2125, 0,3000, 0,0125, 0,3625, 0,1125, 0,0000] | 1,0000 | 65,0 | 47,8250 |

Validação: a soma foi 1,0 nos três casos. Nenhuma AZ passou de 75 °C.

**Robustez (30 sementes):**

| População | Fitness médio | Desvio | Melhor |
|---|---|---|---|
| 10 | 47,8516 | 0,1126 | 47,8250 |
| 30 | 47,8487 | 0,1132 | 47,8250 |
| 50 | 47,8289 | 0,0039 | 47,8250 |

**Validação externa.** Um solver SLSQP (scipy) resolve o mesmo problema e dá exatamente W* = [0,2125, 0,30, 0,0125, 0,3625, 0,1125, 0] e fitness 47,825. Portanto, o PSO com 30 e 50 partículas atingiu o ótimo.

**Análise.**
- Populações maiores convergem de forma mais estável: com 50 partículas o desvio entre execuções cai de ~0,11 para ~0,004. Com 10 partículas, a execução da tabela ficou presa em um ótimo local (48,46).
- O ótimo evita carregar a AZ 6 (a mais quente, coeficiente 65) e a AZ 3 (58). O termo quadrático 40·w² empurra para espalhar a carga nas AZs frias.
- A penalidade externa nunca foi ativada no ótimo: o limite de 75 °C só seria violado se a AZ 6 recebesse mais de 25% da carga. Ela atua nas partículas iniciais, afastando-as dessa região.
- Gráfico: `lab01_fitness.png`.

---

## Lab 02 — AG binário: seleção de microsserviços em Edge

**Dados (premissa).** 15 serviços com valor, RAM e CPU fixos em `lab02_aula08.py`; limites 16 GB de RAM e 8 cores.

**AG.** População 60, 80 gerações, torneio k = 3, crossover de ponto único (pc = 0,85), mutação bit a bit (pm = 0,02), elitismo de 1 indivíduo. 30 sementes por estratégia.
- **A (rígida):** violou RAM ou CPU → fitness 0.
- **B (proporcional):** `fitness = max(0, valor − V_total·(exc_RAM/16 + exc_CPU/8))`.

**Ótimo global (força bruta, 2¹⁵ combinações):** valor 290, serviços {2, 4, 6, 10, 11, 13, 14} (RAM 16,0 GB; CPU 8,0 cores).

| Métrica (30 execuções) | Estratégia A | Estratégia B |
|---|---|---|
| Melhor valor viável, média ± desvio | 283,0 ± 6,7 | 285,2 ± 5,8 |
| Execuções que acharam o ótimo (290) | 13 / 30 | 17 / 30 |
| Melhor combinação final | {2, 4, 6, 10, 11, 13, 14} = 290 | {2, 4, 6, 10, 11, 13, 14} = 290 |
| Diversidade (Hamming médio normalizado) — inicial | 0,500 | 0,500 |
| Diversidade — média das gerações | 0,0955 | 0,0909 |
| Diversidade — final | 0,0491 | 0,0452 |
| Fração de viáveis na população final | 83,7% | 84,8% |

Gráficos (fitness médio ± desvio, desvio-padrão e diversidade por geração): `lab02_comparacao.png`.

**Análise.**
- **Diversidade:** a Estratégia A preservou um pouco mais de diversidade (0,0955 vs 0,0909 na média; 0,049 vs 0,045 no final). Como todos os inviáveis valem 0, o tornei não distingue "quase viável" de "muito inviável" e a seleção é menos direcional. A diferença, porém, é pequena; nas duas estratégias a população converge bastante até a geração 80.
- **Melhor combinação:** a Estratégia B foi mais eficiente. Achou o ótimo em 17 de 30 execuções (contra 13) e teve média melhor. A penalidade proporcional dá gradiente a soluções logo acima do limite, permitindo caminhar até a fronteira de viabilidade, onde está o ótimo (ele usa 100% da RAM e da CPU).
- Ambas encontraram a mesma melhor combinação (valor 290) quando acertaram.
- Observação: o fitness médio da A aparece mais baixo no gráfico porque os inviáveis contam como 0.

---

## Lab 03 — ACO para topologia de rede de baixa latência

**Dados (premissa).** D (10×10) simétrica, gerada com semente fixa (latências de ~7 a ~35 ms). Pares críticos (origem, destino, peso): (0,9,3), (1,8,2), (2,7,3), (3,6,1), (4,5,2), (0,5,2), (1,6,1), (3,9,2).
**Custo de uma árvore** = Σ peso · latência do caminho único entre o par na árvore. (Se o custo fosse só a soma das arestas, o problema seria uma MST trivial.)

**ACO.** 20 formigas, 100 iterações, α = 1, β = 3. Cada formiga parte de um switch aleatório e expande a árvore escolhendo uma aresta (nó na árvore → nó fora da árvore) com probabilidade ∝ τ^α·η^β, η = 1/D. Isso impede ciclos e mantém a conectividade por construção; além disso, toda solução passa por um `assert` de validação (N−1 arestas, sem ciclos, conexa via union-find).
**Feromônio:** apenas as arestas das 3 melhores topologias da iteração são atualizadas, com `τ ← (1−ρ)·τ + ρ·Q/custo`, ρ = 0,2 (τ limitado a [0,01; 10]).

**Matriz de adjacência final (10×10), semente 1:**

```
[[0 0 0 0 0 0 0 1 0 1]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 0 0 1 0 1 0 0 0]
 [0 0 0 0 0 1 0 1 0 0]
 [1 1 1 1 0 0 1 0 1 0]
 [0 0 0 0 0 0 0 1 0 0]
 [1 0 0 0 0 0 0 0 0 0]]
```

Arestas: (0,7) (0,9) (1,7) (2,7) (3,7) (4,5) (5,6) (6,7) (7,8) — 9 arestas, árvore válida, latência total de cabeamento 134,7 ms. O switch 7 funciona como hub central.

| Topologia | Custo (ms ponderados) |
|---|---|
| ACO (semente 1) | 395,7 |
| Aleatória, média de 1000 árvores (desvio 179,3) | 866,6 |
| MST por cabeamento (Prim) | 525,5 |

**Ganho do ACO vs topologia aleatória: 54,3%** (média das 1000 árvores). Contra a MST, o ganho é de 24,7%.

**Robustez (10 sementes):** custo médio 391,9, desvio 12,4, melhor 370,7. A melhor árvore entre as sementes reduz o custo em ~57% frente à média aleatória. Gráfico de convergência: `lab03_convergencia.png`.

**Análise.** A MST minimiza apenas o cabeamento total e não protege os pares críticos, por isso perde para o ACO. O ACO concentra tráfego em um hub (switch 7) que fica próximo de vários pares críticos. A variação entre sementes (±12) mostra que uma execução isolada pode não atingir o melhor resultado; aumentar formigas ou iterações tende a reduzir esse efeito.
