
=== SIMULAÇÕES DE TESTE DE INFERÊNCIA ===
[Mínimo Absoluto] -> Imp: 0.0% | Exp: 0.0 => Urgência: 10.00%
[Baixo Impacto + Alta Explorabilidade (Transição)] -> Imp: 10.0% | Exp: 9.0 => Urgência: 46.50%
[Médio Impacto + Moderado] -> Imp: 50.0% | Exp: 5.0 => Urgência: 76.67%
[Máximo Absoluto] -> Imp: 100.0% | Exp: 10.0 => Urgência: 92.22%
Sucesso: Imagem 'results/superficie_decisao.png' gerada com êxito!


TESTES ENTRE ABORDAGENS
[ABORDAGEM A] [Mínimo Absoluto] -> Imp: 0.0% | Exp: 0.0 => Urgência: 10.24%
[ABORDAGEM A] [Máximo Absoluto] -> Imp: 100.0% | Exp: 10.0 => Urgência: 93.00%

[ABORDAGEM B - MOM] [Minimo Absoluto] -> Imp: 0.0% | Exp: 0.0 => Urgencia: 0.00%
[ABORDAGEM B - MOM] [Maximo Absoluto] -> Imp: 100.0% | Exp: 10.0 => Urgencia: 95.00%
[ABORDAGEM B - MOM] [Medio Impacto + Moderado] -> Imp: 50.0% | Exp: 5.0 => Urgencia: 80.00%****


RELATÓRIO

Por que o Centroide não atinge as pontas

O método centroid calcula a saída como o centro de massa geométrico da área resultante da agregação de todas as regras ativadas — não o ponto de maior pertinência, mas a média ponderada de toda a área sob a curva.

Quando Impacto=0 e Explorabilidade=0, a regra urgencia['baixa'] dispara com força máxima. Só que urgencia['baixa'] é um triângulo trimf([0, 0, 30]) — ou seja, tem pico em 0, mas sua base se estende até 30. O centroide não “para” na ponta onde está o pico; ele pondera toda a massa da figura, incluindo a parte da base que vai até 30. Geometricamente, o centro de massa de um triângulo reto com vértice em 0 fica a 1/3 da base — por isso seu resultado deu 10.00% (1/3 de 30), e não 0%.

O mesmo acontece no outro extremo: mesmo urgencia['critica'] sendo um trapézio com platô em 100, a rampa de subida (80→90) “puxa” o centroide pra baixo do 100%, porque ainda há área naquela região intermediária contribuindo pro cálculo.

Em resumo: o centroide nunca bate exatamente nas pontas porque ele é uma média de área, não um pico — e qualquer função de pertinência com inclinação (rampa) perto da borda distribui “massa” para fora do extremo, puxando o resultado final pra dentro da escala.

Qual abordagem é melhor

Comparando as três (adapte com seus números reais das rodadas A e B que você já tem):

Original (centroid + triângulo/trapézio padrão): não crava nem 0% nem 100%, mas tem transição suave no meio da escala.
Abordagem A (trapézio nas bordas + centroid): melhora os extremos (fica mais perto de 0/100 que o original), mas não crava exatamente — ainda sobra alguma rampa contribuindo pro centro de massa. Mantém a suavidade de transição no meio, já que o método de cálculo (centroide) continua o mesmo.
Abordagem B (MOM — Mean of Maximum): crava os extremos com mais precisão, porque pega a média dos pontos de máxima pertinência, não a área toda — se o pico (ou platô) está em 100, o MOM tende a resultar bem próximo de 100. Só que isso tem um custo: o MOM é menos suave no meio da escala, porque ele ignora a forma da curva fora do pico e pode gerar saltos/degraus na transição entre regras, ao invés da curva contínua que o centroide produz.


MOTOR DE INFERÊNCIA MAMDANI E SUPERFÍCIE 3D

a) Desafio dos Extremos — Centroide vs. Trapézio/MOM

Por que o Centroide não atinge os extremos (0% e 100%)?

O método centroid calcula a saída como o centro de massa geométrico da área resultante da agregação das regras ativadas — não o ponto de maior pertinência, mas a média ponderada de toda a área sob a curva.

Com Impacto=0 e Explorabilidade=0, a regra impacto['baixo'] & explorabilidade['baixa'] → urgencia['baixa'] dispara com força máxima. A função urgencia['baixa'] é um triângulo (trimf([0, 0, 30])) com pico em 0 e base até 30. O centroide não para na ponta onde está o pico: ele pondera toda a massa da figura, incluindo a base que se estende até 30. Geometricamente, o centro de massa de um triângulo retângulo com vértice em 0 fica a 1/3 da base — por isso o sistema retornou 10.00% (1/3 de 30), e não 0%.

O mesmo ocorre no extremo superior: com Impacto=100 e Explorabilidade=10, a regra aponta para urgencia['critica'] (trapézio [80, 90, 100, 100]). Mesmo havendo um platô em 100, a rampa de subida (80→90) ainda contribui com área para o cálculo do centroide, puxando o resultado para baixo do valor máximo — resultando em 92.22%, e não 100%.

Conclusão: o centroide nunca crava exatamente as pontas porque é uma média de área, não um pico. Qualquer função de pertinência com rampa (inclinação) próxima da borda distribui “massa” para fora do extremo, deslocando o resultado final para dentro da escala.

Abordagem A (trapézio nas bordas + centroid): ao substituir os triângulos das bordas (urgencia['baixa'] e urgencia['critica']) por trapézios com platô mais próximo do extremo, o centroide se aproxima mais de 0%/100%, mas ainda não crava exatamente — a rampa residual do trapézio continua contribuindo com alguma área. Em compensação, a suavidade de transição no meio da escala é mantida, já que o método de cálculo (centro de massa) continua o mesmo.

Abordagem B (MOM — Mean of Maximum): ao trocar o método de defuzzificação para MOM, a saída passa a ser a média dos pontos de pertinência máxima, não mais o centro de massa de toda a área. Isso faz o resultado colar muito mais perto dos extremos quando a regra correspondente satura (grau de pertinência = 1 num platô). O custo é a suavidade: o MOM ignora a forma da curva fora do pico, podendo gerar transições menos contínuas (efeito de “degrau”) entre regras no meio da escala, diferente da curva suave que o centroide produz.

Recomendação: não existe uma abordagem isoladamente superior — há um trade-off entre suavidade no meio da escala (favorece centroide/Abordagem A) e precisão nos extremos (favorece MOM/Abordagem B). A alternativa mais equilibrada é o centroide combinado com trapézios bem dimensionados (Abordagem A com platô mais largo), preservando a continuidade da curva e aproximando os extremos sem o efeito de degrau do MOM.

b) Matriz de Regras 3×3 (9 regras)
Impacto \ Explorabilidade	Baixa (0–4)	Moderada (2–8)	Alta (6–10)
Baixo (0–40)	Urgência Baixa	Urgência Baixa	Urgência Média
Médio (20–80)	Urgência Média	Urgência Alta	Urgência Alta
Alto (60–100)	Urgência Crítica	Urgência Crítica	Urgência Crítica

Codificação (operador & = Fuzzy AND / Mínimo de Mamdani):

python
regra1 = ctrl.Rule(impacto['baixo'] & explorabilidade['baixa'], urgencia['baixa'])
regra2 = ctrl.Rule(impacto['baixo'] & explorabilidade['moderada'], urgencia['baixa'])
regra3 = ctrl.Rule(impacto['baixo'] & explorabilidade['alta'], urgencia['media'])
regra4 = ctrl.Rule(impacto['medio'] & explorabilidade['baixa'], urgencia['media'])
regra5 = ctrl.Rule(impacto['medio'] & explorabilidade['moderada'], urgencia['alta'])
regra6 = ctrl.Rule(impacto['medio'] & explorabilidade['alta'], urgencia['alta'])
regra7 = ctrl.Rule(impacto['alto'] & explorabilidade['baixa'], urgencia['critica'])
regra8 = ctrl.Rule(impacto['alto'] & explorabilidade['moderada'], urgencia['critica'])
regra9 = ctrl.Rule(impacto['alto'] & explorabilidade['alta'], urgencia['critica'])
c) Análise Interpretativa da Superfície de Decisão 3D

A superfície gerada (superficie_decisao.png) representa a saída de Urgência para todas as combinações possíveis de Impacto (eixo X, 0–100%) e Explorabilidade (eixo Y, 0–10), calculadas sobre um grid de 20×20 pontos.

Principais observações:

Continuidade: a superfície é contínua e sem descontinuidades abruptas (saltos ou “degraus”), o que é esperado de um sistema fuzzy com defuzzificação por centroide — cada pequena variação nas entradas gera uma pequena variação suave na saída, sem transições bruscas entre regiões de regras diferentes.
Região de baixo impacto (X próximo de 0): a superfície permanece relativamente baixa e plana, mesmo variando a explorabilidade, refletindo a predominância das regras de “Urgência Baixa/Média” nesse bloco da matriz.
Região de alto impacto (X próximo de 100): a superfície sobe de forma acentuada e satura perto de ~90%, confirmando que a regra “Urgência Crítica” domina esse bloco independentemente da explorabilidade — mas sem atingir exatamente 100%, evidenciando na prática o mesmo “Desafio dos Extremos” discutido no item (a).
Zona de transição (impacto médio): é onde a superfície mostra a inclinação mais acentuada — a urgência cresce rapidamente à medida que a explorabilidade aumenta, mostrando a sensibilidade do sistema nessa faixa intermediária, consistente com as regras 4, 5 e 6 da matriz.
Ausência de platôs artificiais: a suavidade geral confirma que o sistema não apresenta “zonas mortas” — qualquer ponto do espaço de entrada produz uma saída numérica proporcional, validando a cobertura completa das 9 regras (sem lacunas na matriz 3×3).
