import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class MLTuningProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 10.0]), xu=np.array([30.0, 200.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        depth, n_trees = x[0], x[1]
        f1_erro = 0.5 / (depth * np.log10(n_trees))
        f2_latencia_ms = (depth * 0.2) + (n_trees * 0.5)
        out["F"] = [f1_erro, f2_latencia_ms]

res5 = minimize(MLTuningProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=7)

print("=== EXERCICIO 5: Trade-off de Modelos ML ===")
print("Solucoes encontradas:", len(res5.F))
print("Amostra de solucoes (Erro, Latencia):")
for i in range(min(10, len(res5.F))):
    erro = res5.F[i, 0]
    latencia = res5.F[i, 1]
    print("  Erro:", round(erro, 4), "| Latencia:", round(latencia, 2), "ms")

plt.figure(figsize=(7, 4))
plt.scatter(res5.F[:, 0], res5.F[:, 1], color='purple', s=45)
plt.title("Exercicio 5 - Erro vs Tempo de Inferencia (ML)")
plt.xlabel("Erro do Modelo")
plt.ylabel("Tempo de Resposta (ms)")
plt.grid(True)

caminho_saida = "/content/AULA_12/results/exercicio5_pareto.png"
plt.savefig(caminho_saida)
plt.show()
print("Grafico salvo em results/exercicio5_pareto.png")
