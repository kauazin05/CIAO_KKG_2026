"""
LAB 01 - PSO para Balanceamento Dinamico de Carga em Datacenters (AULA 08)

Modelo termico adotado (premissa documentada):
    T_i(w) = C_i + K * w_i      (C_i = coeficiente de aquecimento da AZ, K = 40 °C por 100% de carga)
Fitness (minimizar):
    f(w) = sum_i w_i * T_i(w)  +  penalidade externa
    penalidade = LAMBDA * sum_i max(0, T_i - 75)^2
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])
K = 40.0
T_LIMIT = 75.0
LAMBDA = 1000.0
N_AZ = len(C)


def temperaturas(w):
    return C + K * w


def fitness(w):
    T = temperaturas(w)
    base = float(np.sum(w * T))
    pen = LAMBDA * float(np.sum(np.maximum(0.0, T - T_LIMIT) ** 2))
    return base + pen


def normaliza(w):
    """Operador de normalizacao: projeta no simplex aproximado (w>=0, soma=1)."""
    w = np.maximum(w, 0.0)
    s = w.sum()
    if s <= 1e-12:
        return np.full_like(w, 1.0 / len(w))
    return w / s


class PSO:
    def __init__(self, n_particles, n_iter=150, w_in=0.72, c1=1.49, c2=1.49, seed=0):
        self.n = n_particles
        self.n_iter = n_iter
        self.w_in, self.c1, self.c2 = w_in, c1, c2
        self.rng = np.random.default_rng(seed)

    def run(self):
        rng = self.rng
        X = np.array([normaliza(rng.random(N_AZ)) for _ in range(self.n)])
        V = rng.uniform(-0.1, 0.1, size=(self.n, N_AZ))
        pbest = X.copy()
        pbest_f = np.array([fitness(x) for x in X])
        g_idx = int(np.argmin(pbest_f))
        gbest, gbest_f = pbest[g_idx].copy(), pbest_f[g_idx]
        hist = [gbest_f]
        for _ in range(self.n_iter):
            r1 = rng.random((self.n, N_AZ))
            r2 = rng.random((self.n, N_AZ))
            V = self.w_in * V + self.c1 * r1 * (pbest - X) + self.c2 * r2 * (gbest - X)
            V = np.clip(V, -0.3, 0.3)
            X = X + V
            X = np.array([normaliza(x) for x in X])  # normalizacao a cada iteracao
            for i in range(self.n):
                f = fitness(X[i])
                if f < pbest_f[i]:
                    pbest_f[i] = f
                    pbest[i] = X[i].copy()
                    if f < gbest_f:
                        gbest_f, gbest = f, X[i].copy()
            hist.append(gbest_f)
        return gbest, gbest_f, np.array(hist)


def referencia_otima():
    """Referencia analitica/numerica (SLSQP) para validar a qualidade do PSO."""
    from scipy.optimize import minimize
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    cons += [{"type": "ineq", "fun": (lambda w, i=i: T_LIMIT - (C[i] + K * w[i]))} for i in range(N_AZ)]
    res = minimize(lambda w: float(np.sum(w * (C + K * w))), np.full(N_AZ, 1 / N_AZ),
                   bounds=[(0, 1)] * N_AZ, constraints=cons, method="SLSQP")
    return res.x, res.fun


if __name__ == "__main__":
    resultados = {}
    plt.figure(figsize=(8, 5))
    for n in (10, 30, 50):
        w, f, hist = PSO(n, seed=42).run()
        T = temperaturas(w)
        resultados[n] = dict(W=w.round(4).tolist(), soma=float(w.sum()), fitness=f,
                             Tmax=float(T.max()), hist_inicial=float(hist[0]))
        plt.plot(hist, label=f"{n} particulas")
        print(f"\n=== {n} particulas ===")
        print("W* =", np.round(w, 4), "| soma =", round(float(w.sum()), 10))
        print("Temp por AZ =", np.round(T, 2), "| Tmax =", round(float(T.max()), 2))
        print("Fitness =", round(f, 4))
    plt.xlabel("Iteracao"); plt.ylabel("Melhor fitness (G_best)")
    plt.title("Lab 01 - Evolucao do fitness do PSO por tamanho de populacao")
    plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig("lab01_fitness.png", dpi=120)

    # robustez: 30 sementes por populacao
    print("\n=== Robustez (30 sementes) ===")
    robust = {}
    for n in (10, 30, 50):
        fs = [PSO(n, seed=s).run()[1] for s in range(30)]
        robust[n] = (float(np.mean(fs)), float(np.std(fs)), float(np.min(fs)))
        print(f"{n} part.: media={robust[n][0]:.4f} desvio={robust[n][1]:.4f} melhor={robust[n][2]:.4f}")

    w_ref, f_ref = referencia_otima()
    print("\nReferencia SLSQP: W =", np.round(w_ref, 4), "| fitness =", round(float(f_ref), 4))
    json.dump(dict(resultados=resultados, robustez=robust, ref=dict(W=w_ref.round(4).tolist(), f=float(f_ref))),
              open("lab01_results.json", "w"), indent=1)
