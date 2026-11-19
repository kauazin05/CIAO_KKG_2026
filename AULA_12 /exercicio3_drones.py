import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class DroneProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=3, xl=np.array([10.0, 1.0]), xu=np.array([80.0, 5.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        velocidade, carga = x[0], x[1]
        f1_tempo = 1000.0 / velocidade
        f2_custo = (velocidade ** 2) * 0.1 + (carga * 50)
        f3_co2 = (velocidade * 1.5) / carga
        out["F"] = [f1_tempo, f2_custo, f3_co2]

res3 = minimize(DroneProblem(), NSGA2(pop_size=40), termination=('n_gen', 50), seed=42)

print("=== EXERCICIO 3: Logistica de Drones ===")
print("Solucoes encontradas:", len(res3.F))
print("Amostra de solucoes (Tempo, Custo, CO2):")
for linha in res3.F[:10]:
    tempo = linha[0]
    custo = linha[1]
    co2 = linha[2]
    print("  Tempo:", round(tempo, 2), "min | Custo:", round(custo, 2), "| CO2:", round(co2, 2))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(res3.F[:, 0], res3.F[:, 1], res3.F[:, 2], color='green', s=40)
ax.set_xlabel("Tempo")
ax.set_ylabel("Custo")
ax.set_zlabel("CO2")
plt.title("Exercicio 3 - Pareto 3D: Drones")
plt.savefig('/content/AULA_12/results/exercicio3_pareto3d.png')
plt.show()
print("Grafico salvo em results/exercicio3_pareto3d.png")
