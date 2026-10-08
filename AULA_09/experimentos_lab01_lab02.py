# Experimentos dos Labs 01 (ventilador) e 02 (gorjeta) - Aula 09
import numpy as np, skfuzzy as fuzz
from skfuzzy import control as ctrl
import warnings; warnings.filterwarnings("ignore")

# LAB01
t = ctrl.Antecedent(np.arange(0,41,1),"temperatura"); v = ctrl.Consequent(np.arange(0,101,1),"velocidade")
t["frio"]=fuzz.trapmf(t.universe,[0,0,15,25]); t["morno"]=fuzz.trimf(t.universe,[15,25,35]); t["quente"]=fuzz.trapmf(t.universe,[25,35,40,40])
v["baixa"]=fuzz.trimf(v.universe,[0,0,50]); v["media"]=fuzz.trimf(v.universe,[0,50,100]); v["alta"]=fuzz.trimf(v.universe,[50,100,100])
s=ctrl.ControlSystemSimulation(ctrl.ControlSystem([ctrl.Rule(t["frio"],v["baixa"]),ctrl.Rule(t["morno"],v["media"]),ctrl.Rule(t["quente"],v["alta"])]))
print("LAB01")
for x in [10,20,25,30,38]:
    s.input["temperatura"]=x; s.compute(); print(x, round(s.output["velocidade"],1))

# LAB02
def build(variant="base", method="centroid", rule2="base"):
    sv=ctrl.Antecedent(np.arange(0,10.01,0.1),"servico"); cm=ctrl.Antecedent(np.arange(0,10.01,0.1),"comida")
    g=ctrl.Consequent(np.arange(0,25.01,0.5),"gorjeta",defuzzify_method=method)
    for var in (sv,cm):
        var["ruim"]=fuzz.trimf(var.universe,[0,0,5]); var["medio"]=fuzz.trimf(var.universe,[0,5,10]); var["bom"]=fuzz.trimf(var.universe,[5,10,10])
    if variant=="trap":
        sv["ruim"]=fuzz.trapmf(sv.universe,[0,0,2,5]); sv["medio"]=fuzz.trapmf(sv.universe,[2,4,6,8]); sv["bom"]=fuzz.trapmf(sv.universe,[5,8,10,10])
    if variant=="gauss":
        sv["ruim"]=fuzz.gaussmf(sv.universe,0,2); sv["medio"]=fuzz.gaussmf(sv.universe,5,1.5); sv["bom"]=fuzz.gaussmf(sv.universe,10,2)
    if variant=="exc":
        sv["ruim"]=fuzz.trimf(sv.universe,[0,0,3]); sv["medio"]=fuzz.trimf(sv.universe,[0,3,6]); sv["bom"]=fuzz.trimf(sv.universe,[3,6,9]); sv["excelente"]=fuzz.trimf(sv.universe,[6,10,10])
    g["baixa"]=fuzz.trimf(g.universe,[0,0,13]); g["media"]=fuzz.trimf(g.universe,[0,13,25]); g["alta"]=fuzz.trimf(g.universe,[13,25,25])
    r2 = sv["medio"] if rule2=="base" else sv["medio"]&cm["medio"]
    rules=[ctrl.Rule(sv["ruim"]|cm["ruim"],g["baixa"]),ctrl.Rule(r2,g["media"]),ctrl.Rule(sv["bom"]|cm["bom"],g["alta"])]
    if variant=="exc": rules.append(ctrl.Rule(sv["excelente"],g["alta"]))
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
def run(sim,a,b):
    sim.input["servico"]=a; sim.input["comida"]=b; sim.compute(); return round(sim.output["gorjeta"],2)
print("LAB02 base (7,3):",run(build(),7,3))
print("E1 rule2 &:",run(build(rule2="and"),7,3))
for var in ["trap","gauss"]: print("E2",var,run(build(var),7,3))
for m in ["centroid","bisector","mom","som","lom"]: print("E3",m,run(build(method=m),7,3))
print("E4 exc (7,3):",run(build("exc"),7,3), "(10,10):",run(build("exc"),10,10))
for p in [(0,0),(10,10),(5,5)]: print("E5",p,run(build(),*p))
print("EXTRA (7,1) base:",run(build(),7,1)," and:",run(build(rule2="and"),7,1))
