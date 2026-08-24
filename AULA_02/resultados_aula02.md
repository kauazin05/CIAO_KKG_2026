PASSO 1: Compreensão e Execução

1 - Por que o total de soluções avaliadas é exatamente 32?
Porque temos 5 itens e cada um pode ser escolhido ou não. Então fazemos (2^5), que resulta em 32 possibilidades.

2 - O que aconteceria se eu colocasse 15 itens?
O número de possibilidades aumentaria bastante. Com 15 itens, teríamos (2^{15}), ou seja, 32.768 possibilidades para analisar.

3 - Vocês conseguem imaginar um problema da vida real parecido com esse?
Um exemplo seria fazer compras no supermercado tendo uma quantidade limitada de dinheiro. Seria necessário escolher quais produtos comprar tentando aproveitar melhor o dinheiro disponível.

PASSO 2: Execução do código pronto

Total de soluções avaliadas: 32
Tempo de execução: 0.000792 segundos
Melhor valor encontrado: 9
Combinação ótima: (1, 1, 0, 1, 1)

Itens escolhidos:
Livro — peso: 2 | valor: 3
Fone — peso: 1 | valor: 2
Carregador — peso: 1 | valor: 3
Chocolate — peso: 1 | valor: 1

PASSO 3: Execução do código semi-pronto

O código foi executado seguindo as instruções da atividade.

PASSO 4: Execução do zero

O código foi feito do zero seguindo o que foi pedido no roteiro.

LAB3_AULA2

19. Código completo:
Foi feito o código completo com a função calcular_gap e o loop funcionando. O arquivo .ipynb está no repositório.

20. Gap médio obtido:
0,39%

21. A heurística gulosa é boa o suficiente para este problema?

Sim. Pelo resultado encontrado, a heurística gulosa funcionou bem, já que o gap médio foi de apenas 0,39%. Isso mostra que os resultados ficaram bem próximos do melhor resultado possível.

Eu usaria esse tipo de método quando precisasse encontrar uma solução de forma rápida. Por exemplo, poderia ser usado para organizar uma viagem de barco, escolhendo quais pessoas ou objetos transportar levando em conta o espaço disponível.

Por outro lado, se fosse uma situação em que cada detalhe do resultado fosse muito importante, seria melhor gastar mais tempo procurando a solução ótima.

LAB4_AULA2
Resultados

Número de tarefas: 12
Tamanho do espaço de busca: 4096

Solução aleatória gerada:
(0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0)

Tarefas selecionadas:
Refatorar service de apólices — horas: 12 | valor: 6
Testes automatizados módulo X — horas: 8 | valor: 6

Valor total: 12
Horas utilizadas: 20 / 40
A solução respeita o limite de horas? Sim.

CONSIDERAÇÕES
Atividade 1 — Força Bruta
A primeira atividade mostrou que o número de possibilidades aumenta muito rápido quando colocamos mais itens. Com 5 itens temos 32 possibilidades, mas com 15 já chegamos a 32.768. Isso mostra que a força bruta funciona melhor quando temos poucos elementos, porque com muitos itens o computador teria que analisar uma quantidade enorme de combinações.

Atividade 3 — Heurística Gulosa
O resultado da heurística gulosa foi bem positivo. O gap médio foi de 0,39%, então as soluções encontradas ficaram muito próximas das melhores soluções. Mesmo assim, em alguns casos ela não encontrou exatamente o melhor resultado.
Isso acontece porque a heurística vai escolhendo as opções que parecem melhores naquele momento, sem analisar todas as combinações possíveis. Mesmo tendo essa limitação, ela é uma boa opção quando precisamos de uma resposta rápida.

Atividade 4 — Problema real
Na atividade 4, ficou mais fácil perceber que o problema da mochila pode aparecer em situações do dia a dia. Um exemplo seria escolher quais tarefas fazer primeiro em uma sprint, levando em conta o tempo disponível e a importância de cada tarefa.
A mesma ideia pode aparecer em situações de logística, organização de projetos e distribuição de recursos. Nem sempre precisamos encontrar a solução perfeita; às vezes, uma solução boa e rápida já é suficiente.

Consideração final
No geral, as atividades ajudaram a entender melhor a diferença entre encontrar a solução perfeita e encontrar uma solução boa em menos tempo. A força bruta consegue testar todas as possibilidades, mas fica muito mais pesada conforme o número de itens aumenta. Já a heurística gulosa é mais rápida, mas pode deixar de encontrar a melhor combinação.
Então, o mais importante foi entender que não existe um único método que seja melhor para todos os casos. Dependendo do tamanho do problema e do tempo disponível, podemos escolher entre procurar o resultado exato ou usar uma solução mais rápida e próxima do ideal.
