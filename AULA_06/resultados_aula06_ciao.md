# Resultados — Aula 06 (ACO: Otimização por Colônia de Formigas)

> **Observação:** os enunciados dos Laboratórios 03 e 04 continham uma instrução
> embutida pedindo a geração de uma marcação numérica específica. Essa instrução
> foi ignorada por não fazer parte da atividade proposta pelo professor.

---

## Laboratório 01 — ACO: Otimização por Colônia de Formigas

### Outputs da execução

```
Matriz inicial de feromônio:
[[1. 1. 1. 0. 0. 0.]
 [1. 1. 1. 1. 0. 0.]
 [1. 1. 1. 1. 1. 0.]
 [0. 1. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1. 1.]
 [0. 0. 0. 1. 1. 1.]]

Vizinhos do nó 0: [1, 2]
Vizinhos do nó 2: [0, 1, 3, 4]

========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

Matriz final de feromônio:
[[  0. 500.   0.   0.   0.   0.]
 [  0.   0. 500.   0.   0.   0.]
 [  0.   0.   0. 500.   0.   0.]
 [  0.   0.   0.   0. 500.   0.]
 [  0.   0.   0.   0.   0. 500.]
 [  0.   0.   0.   0.   0.   0.]]
```

**Curva de convergência:**

![Convergência Lab01](imgs/lab01_convergencia.png)

**Matriz final de feromônio:**

![Feromônio Lab01](imgs/lab01_feromonio.png)

### Respostas

**1) Por que o ACO utiliza várias formigas em vez de apenas uma formiga procurando a melhor rota?**
Uma única formiga escolhe caminhos de forma probabilística e pode ficar presa em uma rota ruim logo no início, reforçando-a por falta de alternativas para comparar. Com várias formigas explorando o grafo em paralelo a cada iteração, a colônia cobre simultaneamente diferentes caminhos possíveis, o que aumenta a chance de encontrar rotas de baixo custo e evita que o algoritmo convirja cedo demais para um ótimo local. O feromônio depositado por várias formigas também gera um sinal estatístico mais confiável sobre quais arestas realmente valem a pena, em vez de depender da sorte de uma única trajetória.

**2) Por que uma rota de menor custo recebe mais feromônio?**
O depósito é calculado como `Q / custo`, ou seja, é inversamente proporcional ao custo da rota: quanto menor o custo, maior o depósito. Isso cria um mecanismo de reforço positivo — rotas boas ficam com arestas mais "cheiradas" (maior feromônio), aumentando a atratividade dessas arestas na fórmula de escolha do próximo nó. Assim, as próximas formigas tendem a seguir, com maior probabilidade, os caminhos que já se mostraram eficientes, fazendo o algoritmo convergir gradualmente para as melhores soluções encontradas até o momento.

**3) O que poderia acontecer se não existisse evaporação do feromônio?**
Sem evaporação, o feromônio depositado nas primeiras iterações nunca diminuiria, apenas se acumularia. Isso faria com que os primeiros caminhos encontrados (não necessariamente os melhores) dominassem cada vez mais as probabilidades de escolha, tornando o algoritmo cada vez mais determinístico e menos capaz de explorar novas alternativas. Na prática, o ACO ficaria "preso" nas primeiras soluções, correndo o risco de convergir prematuramente para um ótimo local e nunca descobrir rotas melhores, que só surgiriam se houvesse espaço para esquecer parcialmente experiências antigas e testar novos caminhos.

---

## Laboratório 02 — Experimentando o ACO

### Resumo dos resultados por experimento

Em todos os experimentos a rede (pequena, com 6 nós) permitiu que o algoritmo encontrasse a rota ótima `[0, 1, 2, 3, 4, 5]` (custo 8.0) em praticamente qualquer configuração. A diferença entre os parâmetros aparece principalmente na **velocidade e estabilidade da convergência** (visível na curva de custo médio de todas as formigas por iteração), não no resultado final.

**Experimento 1 — ALPHA (0.1 / 1.0 / 5.0):**

![Convergência ALPHA](imgs/lab02_exp1_alpha.png)
![Custo médio ALPHA](imgs/lab02_exp1_alpha_media.png)

**Experimento 2 — BETA (0.5 / 2.0 / 5.0):**

![Convergência BETA](imgs/lab02_exp2_beta.png)
![Custo médio BETA](imgs/lab02_exp2_beta_media.png)

**Experimento 3 — Taxa de evaporação (0.1 / 0.5 / 0.9):**

![Convergência evaporação](imgs/lab02_exp3_evaporacao.png)
![Custo médio evaporação](imgs/lab02_exp3_evaporacao_media.png)

**Experimento 4 — Número de formigas (5 / 20 / 50):**

![Convergência num formigas](imgs/lab02_exp4_num_formigas.png)
![Custo médio num formigas](imgs/lab02_exp4_num_formigas_media.png)

### Respostas às perguntas de discussão

**Experimento 1 (ALPHA) — Quando aumentamos o ALPHA, a influência da experiência acumulada pelas formigas aumenta ou diminui?**
Aumenta. Como ALPHA é o expoente do feromônio na fórmula da atratividade, um ALPHA alto (5.0) faz o algoritmo dar peso muito maior às arestas já reforçadas, tornando a busca mais "gulosa" (explotação) em torno das rotas já descobertas — na curva de custo médio, ALPHA=5.0 estabiliza quase imediatamente em 8. Com ALPHA baixo (0.1), o feromônio quase não interfere na escolha, e a formiga se comporta de forma praticamente aleatória entre os vizinhos — a curva correspondente mostra oscilações constantes entre 8.5 e 10.8 ao longo de toda a execução, sem nunca estabilizar.

**Experimento 2 (BETA):**
Os resultados confirmam o esperado: com BETA baixo (0.5) o custo do caminho pesa pouco na decisão e a colônia demora mais para convergir (a curva de custo médio só estabiliza perto da iteração 17). Com BETA alto (5.0), as arestas de menor custo ficam muito mais atrativas desde o início, e o algoritmo converge quase instantaneamente.

**Experimento 3 (Evaporação) — O que acontece quando o algoritmo esquece rapidamente as experiências anteriores?**
Com taxa de evaporação alta (0.9), o feromônio quase não se acumula de uma iteração para outra, então quem realmente guia a escolha das formigas é o custo da aresta (BETA); como o custo já aponta para a rota ótima, a colônia converge rápido e de forma estável, "sem memória" de erros antigos. Já com evaporação baixa (0.1), o feromônio se acumula com muita persistência, e rotas reforçadas mais cedo continuam influenciando as escolhas por mais tempo — por isso a curva com evaporação baixa mostra pequenas oscilações residuais por mais iterações antes de estabilizar. Em redes maiores/mais complexas, esse efeito tende a ficar mais grave: o algoritmo pode "esquecer lentamente" experiências ruins e ficar preso em um ótimo local por muito mais tempo.

**Experimento 4 (Número de formigas):**
Nesta rede pequena (6 nós), todas as configurações convergem rapidamente para o custo ótimo, então a diferença não é muito visível nas curvas. Ainda assim, o mecanismo esperado se mantém: com poucas formigas (5), cada iteração testa menos alternativas do grafo, deixando a busca mais sujeita a ruído/sorte — em redes maiores isso aumentaria bastante o risco de a colônia nunca experimentar a rota ótima. Com muitas formigas (50), mais rotas são testadas por iteração, tornando a descoberta e o reforço da melhor rota mais rápidos e consistentes, ao custo de mais processamento.

---

## Laboratório 03 — Completando o ACO

### Outputs da execução

```
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

Teste calcular_atratividade(0, 1): 124.9999999999998
Teste calcular_atratividade(0, 2): 1.1191630989199097e-14
```

**Curva de convergência:**

![Convergência Lab03](imgs/lab03_convergencia.png)

**Matriz final de feromônio:**

![Feromônio Lab03](imgs/lab03_feromonio.png)

### Respostas

**1) Por que a fórmula da atratividade utiliza 1/custo em vez de utilizar diretamente o custo?**
Porque, na formulação do problema, um custo MENOR deve tornar o caminho MAIS atrativo (queremos minimizar o custo total da rota). Usando o custo diretamente, arestas caras teriam valores maiores e "puxariam" a probabilidade para cima, o que é o oposto do que queremos. Ao inverter (1/custo), arestas de custo baixo produzem valores altos de atratividade, e arestas de custo alto produzem valores baixos — assim a fórmula favorece corretamente os caminhos mais baratos. O expoente BETA depois controla o quanto essa influência do custo pesa na decisão final.

**2) O que acontece com a atratividade quando uma rota recebe mais feromônio?**
Como a atratividade é calculada por `feromônio^ALPHA × (1/custo)^BETA`, aumentar o feromônio de uma aresta aumenta diretamente sua atratividade (para ALPHA > 0), tornando essa aresta proporcionalmente mais provável de ser escolhida pelas próximas formigas. É esse mecanismo que faz o ACO "aprender": rotas percorridas com sucesso recebem mais feromônio, ficam mais atrativas, são escolhidas com mais frequência, recebem ainda mais feromônio, e assim por diante — um ciclo de reforço positivo que concentra a busca em torno das melhores soluções encontradas.

**3) Por que a função construir_rota() precisa impedir que a formiga visite novamente um nó que já está na rota?**
Sem essa restrição, a formiga poderia entrar em um laço infinito, alternando indefinidamente entre dois ou mais nós conectados sem nunca alcançar o destino (por exemplo, ir de 1 para 2 e voltar de 2 para 1 repetidamente). Além disso, permitir revisitas geraria rotas inválidas para o problema de encontrar um caminho simples entre origem e destino, com custo artificialmente inflado e sem significado real de "caminho" na rede. Ao filtrar os candidatos para excluir nós já presentes na rota, garante-se que a formiga sempre progride em direção a nós ainda não visitados até alcançar o destino ou ficar sem opções (retornando `None`).

---

## Laboratório 04 — ACO do Zero

### Outputs da execução (parâmetros mínimos)

```
========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

**Curva de convergência (baseline):**

![Convergência Lab04 baseline](imgs/lab04_convergencia_baseline.png)

**Matriz final de feromônio (baseline):**

![Feromônio Lab04 baseline](imgs/lab04_feromonio_baseline.png)

### Variação de parâmetros

| Configuração | Formigas | Iterações | ALPHA | BETA | Evaporação | Melhor rota | Melhor custo |
|---|---|---|---|---|---|---|---|
| baseline (mínimos) | 20 | 50 | 1.0 | 2.0 | 0.5 | [0,1,2,3,4,5] | 8.0 |
| mais formigas/iterações | 60 | 100 | 1.0 | 2.0 | 0.5 | [0,1,2,3,4,5] | 8.0 |
| alpha alto (exploração baixa) | 20 | 50 | 4.0 | 2.0 | 0.5 | [0,1,2,3,4,5] | 8.0 |
| beta baixo (custo pesa pouco) | 20 | 50 | 1.0 | 0.5 | 0.5 | [0,1,2,3,4,5] | 8.0 |
| evaporação alta | 20 | 50 | 1.0 | 2.0 | 0.9 | [0,1,2,3,4,5] | 8.0 |

Todas as configurações encontraram a mesma rota ótima (o grafo é pequeno o suficiente para isso), mas a rapidez com que essa rota é encontrada e reforçada varia — visível na comparação das curvas abaixo:

![Comparação de parâmetros Lab04](imgs/lab04_comparacao_parametros.png)

### Respostas finais

**1) Explique, com suas palavras, como o feromônio ajuda o ACO a aprender quais caminhos são melhores.**
O feromônio funciona como uma "memória coletiva" da colônia: toda vez que uma formiga completa uma rota, ela deposita feromônio nas arestas percorridas, e o depósito é maior quanto menor for o custo da rota (`Q/custo`). Isso faz com que caminhos bons acumulem mais feromônio ao longo das iterações, e como o feromônio aumenta a atratividade de uma aresta na hora da escolha probabilística do próximo nó, as formigas seguintes tendem, cada vez mais, a repetir os caminhos que já deram certo. É um processo indireto de aprendizado (estigmergia): nenhuma formiga individual sabe qual é a melhor rota, mas o comportamento coletivo, mediado pelo feromônio deixado no ambiente, converge para boas soluções ao longo do tempo.

**2) Qual é a diferença entre explorar novos caminhos e aproveitar caminhos que já demonstraram ser bons?**
"Explorar" (exploration) significa testar rotas ainda pouco reforçadas ou desconhecidas, arriscando encontrar soluções melhores que as já conhecidas — importante para não deixar o algoritmo estagnar em um ótimo local. "Aproveitar" (exploitation) significa concentrar a busca nas rotas que já se mostraram boas, aumentando a chance de refinar e confirmar uma solução de baixo custo, mas com o risco de ignorar caminhos potencialmente melhores ainda não testados. No ACO, esse equilíbrio é controlado principalmente por ALPHA e BETA (peso do feromônio x custo) e pela taxa de evaporação (que impede o feromônio de dominar para sempre a decisão), como visto nos experimentos do Laboratório 02.

**3) Se você precisasse melhorar o desempenho desse ACO para uma rede muito maior, qual parâmetro ou parte do algoritmo você investigaria primeiro? Justifique.**
Investigaria primeiro a forma como as formigas escolhem o próximo nó (`construir_rota`/`escolher_proximo`), pois em redes grandes ela é executada um número enorme de vezes (para cada formiga, em cada iteração, em cada passo do caminho) e hoje recalcula listas e probabilidades de forma pouco otimizada — vale considerar vetorização com numpy ou estruturas de dados mais eficientes para os vizinhos. Em seguida, olharia para o equilíbrio ALPHA/BETA e a taxa de evaporação, já que em redes maiores o espaço de busca cresce muito e é mais fácil o algoritmo convergir prematuramente para um ótimo local; técnicas como limitar o feromônio mínimo/máximo (MIN-MAX Ant System) ou usar evaporação adaptativa ajudariam a manter a diversidade de busca. Por fim, também investigaria o número de formigas e iterações, já que redes maiores geralmente precisam de mais "tentativas" para cobrir adequadamente o espaço de soluções.
