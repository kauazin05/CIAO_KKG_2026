# AULA 13 - Exercicio 6: Pipeline Completo - Otimizacao + Restricao + MCDM
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize
from pymoo.mcdm.pseudo_weights import PseudoWeights

LIMITE_ESPERA = 25.0  # SLA hospitalar (minutos)


class EscalaHospitalarProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Medicos Plantonistas (2 a 20), x2: Enfermeiros (4 a 40)
        # TODO 1: 2 variaveis inteiras, 2 objetivos e 1 restricao de desigualdade
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([2, 4]),
            xu=np.array([20, 40]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        medicos, enfermeiros = x[0], x[1]

        # Objetivo 1: Custo do Plantao (R$)
        f1_custo = (medicos * 1200.0) + (enfermeiros * 450.0)

        # Objetivo 2: Tempo Medio de Espera na Triagem (minutos)
        f2_espera = (180.0 / medicos) + (240.0 / enfermeiros)

        # TODO 2: SLA -> f2_espera <= 25  =>  G(x) = f2_espera - 25 <= 0
        g1 = f2_espera - LIMITE_ESPERA

        out["F"] = [f1_custo, f2_espera]
        out["G"] = [g1]


# TODO 3: NSGA2 com operadores inteiros (pop_size=40), 50 geracoes
algorithm = NSGA2(
    pop_size=40,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True
)
res6 = minimize(EscalaHospitalarProblem(), algorithm, ('n_gen', 50), seed=42)

if res6.F is None:
    raise RuntimeError("Nenhuma solucao viavel encontrada para o SLA de 25 minutos.")

print(f"Solucoes viaveis na fronteira: {len(res6.F)}")

# TODO 4: PseudoWeights [0.40 custo, 0.60 espera]
pesos = np.array([0.40, 0.60])
idx = PseudoWeights(pesos).do(res6.F)

medicos, enfermeiros = res6.X[idx].astype(int)
custo, espera = res6.F[idx]

assert espera <= LIMITE_ESPERA, "Solucao escolhida viola o SLA!"

print("\nEscala Recomendada (40% Custo / 60% Tempo de Espera):")
print(f"-> Medicos plantonistas: {medicos}")
print(f"-> Enfermeiros:          {enfermeiros}")
print(f"-> Custo do plantao:     R$ {custo:,.2f}")
print(f"-> Tempo medio espera:   {espera:.2f} min (SLA <= {LIMITE_ESPERA:.0f} min: OK)")
