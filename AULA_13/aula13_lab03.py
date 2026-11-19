# AULA 13 - Exercicio 3: Operadores Geneticos (Exploracao vs. Explotacao)
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize


class BenchmarkTradeoffProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([0.1, 0.1]), xu=np.array([10.0, 10.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0]**2 + x[1]
        f2 = (10.0 / x[0]) + (5.0 / x[1])
        out["F"] = [f1, f2]


problem = BenchmarkTradeoffProblem()

# Configuracao A: Exploracao agressiva (eta baixo = filhos distantes dos pais)
alg_exploracao = NSGA2(
    pop_size=30,
    crossover=SBX(prob=0.9, eta=5),
    mutation=PM(prob=0.5, eta=5)
)

# Configuracao B: Explotacao refinada (eta alto = filhos muito proximos dos pais)
alg_explotacao = NSGA2(
    pop_size=30,
    crossover=SBX(prob=0.9, eta=30),
    mutation=PM(prob=0.05, eta=30)
)

res_a = minimize(problem, alg_exploracao, ('n_gen', 20), seed=42)
res_b = minimize(problem, alg_explotacao, ('n_gen', 20), seed=42)

print(f"Config A (exploracao): {len(res_a.F)} solucoes | "
      f"f1 em [{res_a.F[:,0].min():.2f}, {res_a.F[:,0].max():.2f}]")
print(f"Config B (explotacao): {len(res_b.F)} solucoes | "
      f"f1 em [{res_b.F[:,0].min():.2f}, {res_b.F[:,0].max():.2f}]")

plt.figure(figsize=(8, 5))
plt.scatter(res_a.F[:, 0], res_a.F[:, 1], color='orange', label='Config A: Alta Exploracao (eta=5)', alpha=0.8, s=60)
plt.scatter(res_b.F[:, 0], res_b.F[:, 1], color='navy', marker='x', label='Config B: Alta Explotacao (eta=30)', s=60)
plt.title("Exercicio 3 - Efeito dos Parametros SBX/PM em 20 Geracoes")
plt.xlabel("Objetivo 1 [Minimizar]")
plt.ylabel("Objetivo 2 [Minimizar]")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("aula13_lab03.png", dpi=120)
plt.show()
