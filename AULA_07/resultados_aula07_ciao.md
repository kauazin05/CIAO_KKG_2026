LAB 01 -
1. As formigas exploram caminhos meio no achismo, e o 2-opt entra depois refinando cada rota até não dar mais para melhorar. Isso acelera muito a convergência, mas o preço é que todo mundo tende a convergir pro mesmo caminho, arriscando travar numa solução que não é a ideal.
2. Sem evaporação, o feromônio nunca seria esquecido — nem os erros do início. O algoritmo ficaria preso repetindo sempre a mesma rota, mesmo existindo uma melhor.

LAB 02 -
1. A mutação evita que a população fique estagnada, trazendo variedade de volta. Só que com 100% de mutação vira bagunça total: cada filho vira o oposto de si mesmo e todo aprendizado dos pais se perde.
2. A penalização (zerar quem estoura o peso) é essencial porque o algoritmo sozinho não sabe "trapacear" — sem ela, adoraria uma solução impossível de usar na prática.

LAB 03 -
1. Sem a memória própria da partícula (c1=0), ela para de confiar na própria experiência e só segue o grupo — converge rápido, mas fica arriscado se o ponto seguido for ruim, porque ninguém mais questiona.
2. A inércia é tipo um freio de mão: alta, deixa as partículas mais soltas explorando; baixa, faz elas pararem de vagar e refinarem o que já acharam.

LAB 04 -
1. A evaporação evita que o algoritmo "vicie" num caminho só porque foi usado uma vez, apagando aos poucos o rastro das rotas ruins.
2. Sem ela, em redes grandes o algoritmo ficaria grudado nas primeiras decisões para sempre. E quanto menor a latência de um caminho, mais atraente ele é — é só o inverso da latência (1/latência).

LAB 05 -
1. O AG puro só aprende entre gerações (pela reprodução); o memético deixa cada indivíduo "estudar sozinho" antes de reproduzir, refinando a própria solução.
2. Isso acelera a convergência, mas custa caro: fazer todo mundo estudar a cada geração multiplica muito o esforço computacional (no exemplo, cerca de 21x mais caro) — por isso, na prática, costuma-se aplicar isso só numa parte da população.
