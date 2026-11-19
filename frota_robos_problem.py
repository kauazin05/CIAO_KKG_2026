
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize


class FrotaRobosProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([5.0, 1.0]),
            xu=np.array([50.0, 4.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        n_robos, velocidade = x[0], x[1]

        f1_custo = n_robos * 25.0 + (velocidade ** 2) * 8.0
        f2_tempo_ciclo = 120.0 / n_robos + 40.0 / velocidade

        consumo = n_robos * (velocidade ** 1.5)
        g1 = consumo - 120.0

        out["F"] = [f1_custo, f2_tempo_ciclo]
        out["G"] = [g1]


problem = FrotaRobosProblem()

algorithm = NSGA2(pop_size=40)

resultado = minimize(
    problem,
    algorithm,
    ("n_gen", 60),
    seed=10,
    verbose=False
)

if resultado.X is None or resultado.F is None:
    raise RuntimeError("Nenhuma solucao viavel foi encontrada.")

X = np.atleast_2d(resultado.X)
F = np.atleast_2d(resultado.F)

print("=== EXERCICIO 7: Dimensionamento de Frota de Robos ===")
print("Solucoes nao dominadas encontradas:", len(F))

ordem = np.argsort(F[:, 0])
F_ord = F[ordem]
X_ord = X[ordem]

idx_menor_custo = 0
idx_menor_tempo = len(F_ord) - 1
idx_intermediario = len(F_ord) // 2

print("")
print("--- Solucao A: Menor Custo ---")
print("N robos:", round(X_ord[idx_menor_custo, 0], 2))
print("Velocidade:", round(X_ord[idx_menor_custo, 1], 2), "m/s")
print("Custo:", round(F_ord[idx_menor_custo, 0], 2), "mil R$")
print("Tempo de ciclo:", round(F_ord[idx_menor_custo, 1], 2), "min")

print("")
print("--- Solucao B: Menor Tempo de Ciclo ---")
print("N robos:", round(X_ord[idx_menor_tempo, 0], 2))
print("Velocidade:", round(X_ord[idx_menor_tempo, 1], 2), "m/s")
print("Custo:", round(F_ord[idx_menor_tempo, 0], 2), "mil R$")
print("Tempo de ciclo:", round(F_ord[idx_menor_tempo, 1], 2), "min")

print("")
print("--- Solucao C: Intermediaria (equilibrio) ---")
print("N robos:", round(X_ord[idx_intermediario, 0], 2))
print("Velocidade:", round(X_ord[idx_intermediario, 1], 2), "m/s")
print("Custo:", round(F_ord[idx_intermediario, 0], 2), "mil R$")
print("Tempo de ciclo:", round(F_ord[idx_intermediario, 1], 2), "min")

plt.figure(figsize=(8, 6))
plt.scatter(F[:, 0], F[:, 1], s=40, color="teal", label="Solucoes nao dominadas")
plt.scatter(
    [F_ord[idx_menor_custo, 0], F_ord[idx_intermediario, 0], F_ord[idx_menor_tempo, 0]],
    [F_ord[idx_menor_custo, 1], F_ord[idx_intermediario, 1], F_ord[idx_menor_tempo, 1]],
    s=120, color="red", marker="X", label="Solucoes destacadas (A, C, B)"
)
plt.xlabel("Custo Total (mil R$)")
plt.ylabel("Tempo Medio de Ciclo (min)")
plt.title("Exercicio 7 - Fronteira de Pareto: Frota de Robos AMR")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

caminho_saida = "/content/AULA_12/results/exercicio7_pareto.png"
plt.savefig(caminho_saida)
plt.show()
print("")
print("Grafico salvo em results/exercicio7_pareto.png")
