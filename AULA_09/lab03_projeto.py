# ==============================================================================
# AULA 09 - LAB 03: SISTEMA FUZZY DE RISCO DE EVASAO ESCOLAR
# Entradas : frequencia (%) e desempenho (nota 0-10)
# Saida    : risco de evasao (0-100 pontos)
# Execucao : python lab03_projeto_evasao.py
# Requer   : pip install numpy matplotlib scikit-fuzzy
# ==============================================================================
import numpy as np
import matplotlib
matplotlib.use("Agg")  # salva os graficos em PNG (nao abre janela)
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1) UNIVERSOS DE DISCURSO
frequencia = ctrl.Antecedent(np.arange(0, 100.1, 0.5), "frequencia")   # % de presenca
desempenho = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "desempenho")   # nota media
risco = ctrl.Consequent(np.arange(0, 100.1, 1), "risco")               # pontos 0-100

# 2) FUNCOES DE PERTINENCIA
frequencia["baixa"] = fuzz.trapmf(frequencia.universe, [0, 0, 55, 70])
frequencia["media"] = fuzz.trimf(frequencia.universe, [60, 75, 88])
frequencia["alta"] = fuzz.trapmf(frequencia.universe, [80, 90, 100, 100])

desempenho["baixo"] = fuzz.trapmf(desempenho.universe, [0, 0, 3, 5.5])
desempenho["medio"] = fuzz.trimf(desempenho.universe, [4, 6, 8])
desempenho["alto"] = fuzz.trapmf(desempenho.universe, [6.5, 8, 10, 10])

risco["baixo"] = fuzz.trimf(risco.universe, [0, 0, 40])
risco["medio"] = fuzz.trimf(risco.universe, [20, 50, 80])
risco["alto"] = fuzz.trimf(risco.universe, [60, 100, 100])

# 3) BASE DE REGRAS (| = OU, & = E)
regras = [
    ctrl.Rule(frequencia["baixa"] & desempenho["baixo"], risco["alto"]),    # R1
    ctrl.Rule(frequencia["alta"] | desempenho["alto"], risco["baixo"]),     # R2 (OU)
    ctrl.Rule(frequencia["alta"] & desempenho["alto"], risco["baixo"]),     # R3
    ctrl.Rule(frequencia["media"] & desempenho["medio"], risco["medio"]),   # R4
    ctrl.Rule(frequencia["alta"] & desempenho["medio"], risco["baixo"]),    # R5
    ctrl.Rule(frequencia["media"] & desempenho["alto"], risco["baixo"]),    # R6
    ctrl.Rule(frequencia["baixa"] & desempenho["medio"], risco["alto"]),    # R7
    ctrl.Rule(frequencia["media"] & desempenho["baixo"], risco["alto"]),    # R8
    ctrl.Rule(frequencia["alta"] & desempenho["baixo"], risco["medio"]),    # R9
    ctrl.Rule(frequencia["baixa"] & desempenho["alto"], risco["medio"]),    # R10
]

# 4) SISTEMA DE CONTROLE
sistema = ctrl.ControlSystem(regras)


def calcular_risco(freq, nota):
    """Retorna o risco de evasao (0-100) para uma frequencia (%) e uma nota (0-10)."""
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input["frequencia"] = freq
    sim.input["desempenho"] = nota
    sim.compute()
    return sim.output["risco"], sim


def classificar(valor):
    return "BAIXO" if valor < 35 else ("MEDIO" if valor < 65 else "ALTO")


# 5) TESTES (entrada, resposta esperada)
casos = [
    ("Aluno exemplar",          95, 9.0, "BAIXO"),
    ("Faltoso e com notas ruins", 40, 2.0, "ALTO"),
    ("Aluno mediano",           75, 6.0, "MEDIO"),
    ("Bom de nota, mas faltoso", 50, 9.0, "MEDIO"),
    ("Presente, mas nota baixa", 95, 2.5, "MEDIO"),
    ("Frequencia media, nota baixa", 75, 3.0, "ALTO"),
]

if __name__ == "__main__":
    print(f"{'Caso':32}{'Freq':>6}{'Nota':>6}{'Risco':>8}  {'Obtido':8}{'Esperado':8}")
    for nome, f, n, esperado in casos:
        r, _ = calcular_risco(f, n)
        print(f"{nome:32}{f:>5}%{n:>6}{r:>8.1f}  {classificar(r):8}{esperado:8}")

    # 6) GRAFICOS (salvos em PNG)
    frequencia.view(); plt.savefig("grafico_frequencia.png", dpi=120)
    desempenho.view(); plt.savefig("grafico_desempenho.png", dpi=120)
    risco.view(); plt.savefig("grafico_risco.png", dpi=120)
    _, sim = calcular_risco(40, 2.0)
    risco.view(sim=sim); plt.savefig("grafico_resultado_exemplo.png", dpi=120)
    print("\nGraficos salvos em PNG.")
