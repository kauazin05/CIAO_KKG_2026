import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class SOCAllocationProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([1.0, 1.0]),
            xu=np.array([50.0, 10.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        analistas, regimento = x[0], x[1]

        f1_custo = analistas * 100.0 + regimento * 50.0
        f2_tempo = 200.0 / analistas + 50.0 / regimento

        out["F"] = [f1_custo, f2_tempo]

res2 = minimize(SOCAllocationProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=1)

print("=== EXERCICIO 2: Triagem de Incidentes SOC ===")
print(f"Solucoes encontradas: {len(res2.F)}")
print("Amostra de solucoes (Custo, Tempo de Resposta):")
for custo, tempo in res2.F[:10]:
    print(f"  Custo: R$ {custo:.2f} | Tempo: {tempo:.2f} min")
