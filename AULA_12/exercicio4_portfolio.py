import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class PortfolioProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([0.0, 0.0]), xu=np.array([100.0, 100.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        rf, acoes = x[0], x[1]
        retorno = rf * 0.08 + acoes * 0.18
        f1_retorno_negativo = -retorno
        f2_risco = rf * 0.02 + acoes * 0.25
        out["F"] = [f1_retorno_negativo, f2_risco]

res4 = minimize(PortfolioProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=3)

retorno_real = -res4.F[:, 0]
risco = res4.F[:, 1]

print("=== EXERCICIO 4: Selecao de Portfolio ===")
print("Solucoes encontradas:", len(res4.F))
print("Amostra de solucoes (Risco, Retorno Real):")
for i in range(min(10, len(res4.F))):
    print("  Risco:", round(risco[i], 2), "| Retorno:", round(retorno_real[i], 2), "%")

plt.figure(figsize=(7, 4))
plt.scatter(risco, retorno_real, color='orange', s=45)
plt.title("Exercicio 4 - Risco vs Retorno: Portfolio")
plt.xlabel("Risco")
plt.ylabel("Retorno Esperado (%)")
plt.grid(True)

caminho_saida = "/content/AULA_12/results/exercicio4_pareto.png"
plt.savefig(caminho_saida)
plt.show()
print("Grafico salvo em results/exercicio4_pareto.png")
