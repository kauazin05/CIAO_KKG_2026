# AULA 13 - Exercicio 2: Dimensionamento Inteiro de Cluster Kubernetes
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize


class KubernetesClusterProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Replicas da API (2 a 40), x2: Worker Nodes (1 a 12)
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([2, 1]),
            xu=np.array([40, 12]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        replicas, nodes = x[0], x[1]

        # TODO 1: Tempo de Resposta (ms)
        f1_tempo = (600.0 / replicas) + (200.0 / nodes)

        # TODO 2: Custo Mensal (USD)
        f2_custo = (replicas * 12.0) + (nodes * 85.0)

        out["F"] = [f1_tempo, f2_custo]


# TODO 3: NSGA2 com operadores inteiros
algorithm = NSGA2(
    pop_size=25,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True
)

# TODO 4: 35 geracoes, seed=10
res2 = minimize(KubernetesClusterProblem(), algorithm, termination=('n_gen', 35), seed=10)

print(f"Solucoes nao-dominadas encontradas: {len(res2.X)}")
ordem = np.argsort(res2.F[:, 0])
for x, f in zip(res2.X[ordem], res2.F[ordem]):
    print(f"Replicas: {int(x[0]):2d} | Nodes: {int(x[1]):2d} => "
          f"Tempo: {f[0]:7.2f} ms | Custo: US$ {f[1]:7.2f}/mes")
