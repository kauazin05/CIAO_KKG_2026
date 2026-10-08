# Resultados – Aula 09: Lógica Fuzzy
**Disciplina:** Inteligência Computacional

Arquivos desta entrega: `lab03_projeto_evasao.py` (projeto), `experimentos_lab01_lab02.py` (código dos Labs 1 e 2) e os gráficos `grafico_*.png`.

---

## Lab 01 – Ventilador fuzzy (Sprint 1 / AC-3)

### Resultados obtidos

| Temperatura (°C) | Velocidade do ventilador |
|---|---|
| 10 | 17% |
| 20 | 44% |
| 25 | 50% |
| 30 | 56% |
| 38 | 83% |

### O que a lógica fuzzy realiza

Na lógica clássica, uma temperatura é "fria" ou "não fria", sem meio-termo, e o ventilador teria saltos bruscos entre velocidades. A lógica fuzzy trabalha com **graus de pertinência** entre 0 e 1: uma temperatura pode pertencer a vários conjuntos ao mesmo tempo, em graus diferentes. O sistema faz isso em quatro passos:

1. **Fuzzificação:** a temperatura numérica vira graus de pertinência. Em 20 °C, por exemplo, ela é "frio" com grau 0,5 e "morno" com grau 0,5.
2. **Inferência:** as regras SE–ENTÃO disparam proporcionalmente a esses graus (SE frio ENTÃO baixa; SE morno ENTÃO média; SE quente ENTÃO alta). A saída de cada regra é "cortada" no nível do seu grau de ativação.
3. **Agregação:** as saídas das regras são unidas em uma única área.
4. **Defuzzificação:** a área vira um número único (método do centroide), que é a velocidade em %.

O resultado é uma **transição suave**: em 20 °C as regras "frio" e "morno" disparam juntas e a velocidade fica em 44%, valor intermediário entre "baixa" e "média". Em 25 °C (centro de "morno", pertinência 1) a saída é 50%, e em 38 °C o ventilador já está a 83%. Assim a lógica fuzzy imita o raciocínio humano ("está meio quente, ligo um pouco mais forte"), transformando termos vagos em decisões numéricas graduais, sem limites rígidos.

---

## Lab 02 – Experimentos da gorjeta

Caso base: serviço = 7, comida = 3 → **gorjeta = 12,55%** (centroide).

**Experimento 1 – Regra 2 com `servico["medio"] & comida["medio"]`**
Resultado para (7, 3): **12,55%**, ou seja, não mudou. Em serviço = 7, o grau de "médio" é 0,6; em comida = 3, o grau de "médio" também é 0,6. Como o operador E usa o mínimo, min(0,6; 0,6) = 0,6, o mesmo valor da regra original, então a ativação não muda. A diferença aparece quando os graus divergem: para (7, 1), a comida é "média" só com grau 0,2, e o resultado cai de 11,2% para 10,55%. Conclusão: o E deixa a regra mais exigente, pois só dispara forte se as duas condições forem fortes.

**Experimento 2 – Trapézios e gaussianas no serviço**
Para (7, 3): triângulos = 12,55%; trapézios = 13,59%; gaussianas = 12,16%. A mudança numérica é pequena. As gaussianas dão a transição mais suave porque não têm "quinas", então a saída varia de forma contínua quando a nota muda. Os trapézios têm um platô com pertinência 1, onde pequenas variações de nota não alteram o resultado, o que deixa a resposta mais "estável" nessa faixa.

**Experimento 3 – Métodos de defuzzificação (7, 3)**

| Método | Gorjeta |
|---|---|
| centroid | 12,55% |
| bisector | 12,58% |
| mom (média dos máximos) | 12,75% |
| som (menor dos máximos) | 7,80% |
| lom (maior dos máximos) | 17,80% |

Centroide e bisector são parecidos, pois consideram a área inteira. Os métodos baseados em máximos (mom, som, lom) olham apenas o ponto de maior pertinência e por isso são mais bruscos: som e lom dão extremos opostos, pois as regras "baixa" e "alta" disparam ambas com grau 0,4.

**Experimento 4 – Quarto conjunto "excelente" no serviço**
Redistribuí os conjuntos de serviço em ruim [0,0,3], medio [0,3,6], bom [3,6,9] e excelente [6,10,10], e acrescentei a regra:

```python
ctrl.Rule(servico["excelente"], gorjeta["alta"])
```

Resultados: (7, 3) = 13,94% e (10, 10) = 21,0%. A nota alta passa a ter conjunto e regra próprios, o que dá mais controle sobre a faixa de notas altas.

**Experimento 5 – Casos-limite (base)**

| (serviço, comida) | Gorjeta | Esperado? |
|---|---|---|
| (0, 0) | 4,33% | Baixa, como esperado, mas não chega a 0 |
| (10, 10) | 21,0% | Alta, como esperado, mas não chega a 25 |
| (5, 5) | 12,67% | Média, como esperado |

O comportamento é coerente. Os extremos não chegam a 0% e 25% porque o centroide é a média de toda a área do triângulo "cortado", que nunca coincide exatamente com a ponta do universo. Esse é um efeito conhecido do centroide.

---

## Lab 03 – Projeto: Risco de evasão escolar

### Etapa 1 – Definição do problema

O problema é estimar o **risco de evasão de um aluno** a partir da frequência e do desempenho. Hoje quem decide é o professor ou a coordenação, de forma subjetiva ("esse aluno está sumindo e com nota baixa"). As entradas são a **frequência** (% de presença, 0–100) e o **desempenho** (nota média, 0–10). A saída é o **risco de evasão** (0–100 pontos). Fuzzy é adequado porque "frequência baixa" e "desempenho médio" não têm limite exato: um aluno com 74% e outro com 76% de presença são praticamente iguais. Um `if` simples criaria saltos artificiais e não combinaria os dois fatores de modo gradual, como o raciocínio humano.

### Etapa 2 – Modelagem

**Universos de discurso**

| Variável | Tipo | Universo | Unidade |
|---|---|---|---|
| frequencia | entrada | 0 a 100 | % de presença |
| desempenho | entrada | 0 a 10 | nota média |
| risco | saída | 0 a 100 | pontos |

**Termos linguísticos e funções de pertinência**

| Variável | Termo | Forma | Parâmetros |
|---|---|---|---|
| frequencia | baixa | trapézio | [0, 0, 55, 70] |
| frequencia | media | triângulo | [60, 75, 88] |
| frequencia | alta | trapézio | [80, 90, 100, 100] |
| desempenho | baixo | trapézio | [0, 0, 3, 5,5] |
| desempenho | medio | triângulo | [4, 6, 8] |
| desempenho | alto | trapézio | [6,5, 8, 10, 10] |
| risco | baixo | triângulo | [0, 0, 40] |
| risco | medio | triângulo | [20, 50, 80] |
| risco | alto | triângulo | [60, 100, 100] |

**Funções de pertinência (gráficos gerados em código)**

![Frequência](grafico_frequencia.png)

![Desempenho](grafico_desempenho.png)

![Risco](grafico_risco.png)

**Base de regras (10 regras; E em 9 delas, OU na R2)**

| # | Regra |
|---|---|
| R1 | SE frequência **baixa** E desempenho **baixo** ENTÃO risco **alto** |
| R2 | SE frequência **alta** OU desempenho **alto** ENTÃO risco **baixo** |
| R3 | SE frequência **alta** E desempenho **alto** ENTÃO risco **baixo** |
| R4 | SE frequência **média** E desempenho **médio** ENTÃO risco **médio** |
| R5 | SE frequência **alta** E desempenho **médio** ENTÃO risco **baixo** |
| R6 | SE frequência **média** E desempenho **alto** ENTÃO risco **baixo** |
| R7 | SE frequência **baixa** E desempenho **médio** ENTÃO risco **alto** |
| R8 | SE frequência **média** E desempenho **baixo** ENTÃO risco **alto** |
| R9 | SE frequência **alta** E desempenho **baixo** ENTÃO risco **médio** |
| R10 | SE frequência **baixa** E desempenho **alto** ENTÃO risco **médio** |

### Etapa 3 – Implementação

Código-fonte em `lab03_projeto_evasao.py` (NumPy, Matplotlib e scikit-fuzzy). A função `calcular_risco(freq, nota)` devolve o risco calculado. Para executar: `python lab03_projeto_evasao.py`.

### Etapa 4 – Testes

Classificação da saída: **BAIXO** < 35, **MÉDIO** entre 35 e 65, **ALTO** ≥ 65.

| # | Situação | Frequência | Nota | Risco calculado | Obtido | Esperado |
|---|---|---|---|---|---|---|
| 1 | Aluno exemplar | 95% | 9,0 | 13,3 | BAIXO | BAIXO |
| 2 | Faltoso e com notas ruins | 40% | 2,0 | 86,7 | ALTO | ALTO |
| 3 | Aluno mediano | 75% | 6,0 | 50,0 | MÉDIO | MÉDIO |
| 4 | Boa nota, mas faltoso | 50% | 9,0 | 35,7 | MÉDIO | MÉDIO |
| 5 | Presente, mas nota baixa | 95% | 2,5 | 35,7 | MÉDIO | MÉDIO |
| 6 | Frequência média, nota baixa | 75% | 3,0 | 86,7 | ALTO | ALTO |

Resultado visual do caso 2 (frequência 40%, nota 2,0), mostrando a área agregada e a linha do centroide:

![Resultado do caso 2](grafico_resultado_exemplo.png)

**Análise:** nos 6 casos o sistema acertou a faixa esperada. Os casos 4 e 5 ficaram no limite inferior da faixa "médio" (35,7), o que faz sentido: são alunos com um fator bom e outro ruim, e o sistema mistura os dois. Observação honesta: ajustei a regra R2 durante o desenvolvimento. A versão inicial (SE frequência baixa OU desempenho baixo ENTÃO risco médio) conflitava com R1 e puxava os casos graves para a faixa média (o caso 2 dava 64,3). Trocá-la pela regra de risco baixo corrigiu isso.

### Etapa 5 – Entrega

Código-fonte executável: `lab03_projeto_evasao.py`.
