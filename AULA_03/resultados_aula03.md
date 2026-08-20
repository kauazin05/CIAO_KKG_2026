LAB-01 - Compreensão e Execução
Problema:
Encontrar o valor de x que maximiza a função f(x) = x² no intervalo [0, 31], usando uma representação binária de 5 bits.

Resultado da execução:
Na população inicial, o melhor resultado foi:
[1, 1, 1, 0, 1] → x = 29 → f(x) = 841


Na Geração 1, o algoritmo encontrou o melhor resultado possível:
[1, 1, 1, 1, 1] → x = 31 → f(x) = 961


Depois disso, o melhor resultado continuou sendo:
x = 31
f(x) = 961


Resultado final:
Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961
Ótimo global: x = 31, f(x) = 961
Erro: 0


Considerações:
Com a execução, consegui entender melhor como funciona um Algoritmo Genético. No início, o melhor resultado encontrado foi x = 29, com f(x) = 841.
Depois das etapas de seleção, crossover, mutação e elitismo, o algoritmo conseguiu encontrar x = 31 já na Geração 1. Como a função é x² e o intervalo vai de 0 até 31, esse é o melhor resultado possível, chegando a f(x) = 961.
Também deu para perceber a importância do elitismo, porque ele faz com que o melhor resultado encontrado seja mantido nas próximas gerações. Depois que o algoritmo encontrou x = 31, esse resultado continuou sendo o melhor até o final.

LAB-02 - Execução código pronto
Problema:
Encontrar a melhor solução para o problema ONEMAX, utilizando um Algoritmo Genético com 30 indivíduos e 50 gerações.
Nesse problema, o objetivo é encontrar um indivíduo formado por bits 1, buscando maximizar a quantidade de bits iguais a 1. A solução ótima é aquela em que todos os 20 bits são iguais a 1.

Resultado da execução:
Na população inicial, o melhor resultado foi:
Geração 0: Melhor = 14/20, Média = 9.57

Na Geração 10, o algoritmo encontrou um resultado melhor:
Geração 10: Melhor = 19/20, Média = 18.47

Na Geração 20, o algoritmo encontrou o melhor resultado possível:
Geração 20: Melhor = 20/20, Média = 19.63

Depois disso, o melhor resultado continuou sendo:
Geração 30: Melhor = 20/20, Média = 19.63
Geração 40: Melhor = 20/20, Média = 19.57

Resultado final:
MELHOR FITNESS: 20/20
Ótimo = 20 (todos os bits são 1)

Considerações:
Com a execução, deu para perceber como o Algoritmo Genético vai melhorando os resultados ao longo das gerações. No começo, o melhor resultado era 14/20, mas depois foi melhorando aos poucos.
Na Geração 10, chegou a 19/20 e, na Geração 20, conseguiu chegar a 20/20, que é o melhor resultado possível nesse problema.
Depois disso, o resultado continuou em 20/20 nas outras gerações. Isso mostra que o algoritmo conseguiu encontrar a solução ideal, com todos os 20 bits iguais a 1, e manteve esse resultado até o final.

LAB-03 - Execução código semi-pronto
Problema:
Encontrar o valor de x que maximiza a função:
f(x) = x * sin(3x) utilizando um Algoritmo Genético para buscar a melhor solução.

Resultado da execução:
Na população inicial, o melhor resultado encontrado foi:
Geração 0: Melhor f(x) = 6.8149 (x = 6.8235)

Na Geração 10, o algoritmo encontrou um resultado melhor:
Geração 10: Melhor f(x) = 8.9019 (x = 8.9020)

Depois disso, o melhor resultado continuou sendo:
Geração 20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração 30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração 40: Melhor f(x) = 8.9019 (x = 8.9020)

Resultado final:
Melhor x = 8.9020
Melhor f(x) = 8.9019

Considerações:
Com a execução, deu para ver que o algoritmo foi melhorando o resultado. No começo, o melhor valor de f(x) era 6.8149, com x = 6.8235.
Na Geração 10, o resultado melhorou e chegou a 8.9019, com x = 8.9020. Depois disso, o resultado ficou igual nas outras gerações.
Então, o algoritmo encontrou um resultado bem melhor logo no começo e conseguiu manter ele até o final. O melhor resultado foi x = 8.9020, com f(x) = 8.9019.
