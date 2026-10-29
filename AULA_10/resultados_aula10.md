
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
