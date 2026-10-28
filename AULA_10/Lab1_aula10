import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# variaveis do problema
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')
validade = ctrl.Consequent(np.arange(0, 61, 1), 'validade')

# funcoes de pertinencia da temperatura
temperatura['fria'] = fuzz.trapmf(temperatura.universe, [0, 0, 10, 22])
temperatura['amena'] = fuzz.gaussmf(temperatura.universe, 22, 5)
temperatura['quente'] = fuzz.trapmf(temperatura.universe, [25, 30, 40, 40])

# umidade
umidade['baixa'] = fuzz.trapmf(umidade.universe, [0, 0, 20, 60])
umidade['media'] = fuzz.trapmf(umidade.universe, [0, 50, 60, 100])
umidade['alta'] = fuzz.trimf(umidade.universe, [60, 100, 100])

# validade
validade['curta'] = fuzz.trapmf(validade.universe, [0, 0, 5, 30])
validade['aceitavel'] = fuzz.trimf(validade.universe, [10, 30, 50])
validade['longa'] = fuzz.trapmf(validade.universe, [30, 50, 60, 60])

# regras
regra1 = ctrl.Rule(temperatura['fria'] & umidade['baixa'], validade['longa'])
regra2 = ctrl.Rule(temperatura['quente'] | umidade['alta'], validade['curta'])
regra3 = ctrl.Rule(umidade['media'], validade['aceitavel'])

sistema = ctrl.ControlSystem([regra1, regra2, regra3])
simulador = ctrl.ControlSystemSimulation(sistema)

# pede os valores pro usuario
while True:
    temp = float(input('Digite a temperatura (0 a 40 C): '))
    if temp < 0 or temp > 40:
        print('Temperatura fora do intervalo, tenta de novo')
        continue
    break

while True:
    ur = float(input('Digite a umidade (0 a 100 %): '))
    if ur < 0 or ur > 100:
        print('Umidade fora do intervalo, tenta de novo')
        continue
    break

simulador.input['temperatura'] = temp
simulador.input['umidade'] = ur
simulador.compute()

print('A validade e de %d dias' % round(simulador.output['validade']))

# graficos
temperatura.view(sim=simulador)
umidade.view(sim=simulador)
validade.view(sim=simulador)
plt.show()
