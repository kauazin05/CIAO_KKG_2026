
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class EVBatteryProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([10.0, 15.0]),
            xu=np.array([150.0, 45.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        potencia, temp = x[0], x[1]
        f1_tempo_recarga = 3000.0 / potencia
        f2_desgaste_bateria = (potencia ** 1.5) * (temp / 20.0)
        g1 = f2_desgaste_bateria - 1500.0
        out["F"] = [f1_tempo_recarga, f2_desgaste_bateria]
        out["G"] = [g1]

res6 = minimize(EVBatteryProblem(), NSGA2(pop_size=40), termination=("n_gen", 50), seed=5)

print("=== EXERCICIO 6: EV Battery com Restricao ===")
print("Total de solucoes retornadas:", len(res6.F))

if res6.G is not None:
    viaveis_mask = (res6.G[:, 0] <= 0)
    F_viaveis = res6.F[viaveis_mask]
    print("Solucoes viaveis (desgaste <= 1500):", len(F_viaveis))
    print("Amostra de solucoes viaveis (Tempo Recarga, Desgaste):")
    for i in range(min(10, len(F_viaveis))):
        tempo = F_viaveis[i, 0]
        desgaste = F_viaveis[i, 1]
        print("  Tempo:", round(tempo, 2), "min | Desgaste:", round(desgaste, 2))
else:
    F_viaveis = res6.F
    print("Nenhuma restricao retornada; exibindo todas as solucoes.")

plt.figure(figsize=(7, 4))
plt.scatter(F_viaveis[:, 0], F_viaveis[:, 1], color="red", s=45)
plt.title("Exercicio 6 - Tempo de Recarga vs Desgaste")
plt.xlabel("Tempo de Recarga (min)")
plt.ylabel("Desgaste da Bateria")
plt.grid(True)
caminho_saida = "/content/AULA_12/results/exercicio6_pareto.png"
plt.savefig(caminho_saida)
plt.show()
print("Grafico salvo em results/exercicio6_pareto.png")
