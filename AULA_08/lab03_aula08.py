"""
LAB 03 - ACO para Projeto de Topologia de Rede de Baixa Latencia (AULA 08)

Premissas documentadas (o roteiro nao fornece D nem os pares criticos):
  - D (10x10): matriz simetrica de latencias fisicas (ms), gerada com semente fixa a partir de
    posicoes 2D dos switches (latencia ~ distancia + ruido), entre 2 e ~40 ms.
  - Pares criticos: 8 pares (i, j, peso) definidos abaixo.
  - Custo de uma arvore T = soma_{(i,j) criticos} peso * latencia_do_caminho_unico_em_T(i, j).
    (Se o custo fosse so a soma das arestas, o problema seria uma MST trivial.)
  - Evaporacao rho = 0.2 + deposito aplicados apenas as arestas das melhores topologias da iteracao.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 10
rng_d = np.random.default_rng(7)
POS = rng_d.random((N, 2)) * 30
D = np.linalg.norm(POS[:, None] - POS[None, :], axis=2) + 2.0
D = (D + rng_d.random((N, N)) * 4)
D = np.round((D + D.T) / 2, 1)
np.fill_diagonal(D, 0.0)

PARES = [(0, 9, 3.0), (1, 8, 2.0), (2, 7, 3.0), (3, 6, 1.0), (4, 5, 2.0), (0, 5, 2.0), (1, 6, 1.0), (3, 9, 2.0)]

ALPHA, BETA, RHO, Q = 1.0, 3.0, 0.2, 100.0
N_ANTS, N_ITER, TOP_K = 20, 100, 3
TAU_MIN, TAU_MAX = 0.01, 10.0


def caminho_latencia(adj, s, t):
    """Latencia do caminho unico entre s e t na arvore (DFS)."""
    pilha = [(s, -1, 0.0)]
    while pilha:
        u, pai, dist = pilha.pop()
        if u == t:
            return dist
        for v in range(N):
            if adj[u, v] and v != pai:
                pilha.append((v, u, dist + D[u, v]))
    raise ValueError("grafo desconexo")


def custo(arestas):
    adj = np.zeros((N, N), dtype=int)
    for i, j in arestas:
        adj[i, j] = adj[j, i] = 1
    return sum(p * caminho_latencia(adj, i, j) for i, j, p in PARES)


def eh_arvore_valida(arestas):
    """Verifica N-1 arestas, sem ciclos e conectividade (union-find)."""
    if len(arestas) != N - 1:
        return False
    pai = list(range(N))
    def find(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]; x = pai[x]
        return x
    for i, j in arestas:
        ri, rj = find(i), find(j)
        if ri == rj:
            return False  # ciclo
        pai[ri] = rj
    return len({find(x) for x in range(N)}) == 1


def constroi_formiga(tau, rng):
    eta = 1.0 / (D + np.eye(N))
    no_arvore = [int(rng.integers(N))]
    arestas = []
    # Mantem um union-find para vetar ciclos durante a construcao
    while len(no_arvore) < N:
        cand, pesos = [], []
        for u in no_arvore:
            for v in range(N):
                if v not in no_arvore:  # aresta (u,v) nao fecha ciclo e mantem conectividade
                    cand.append((u, v))
                    pesos.append((tau[u, v] ** ALPHA) * (eta[u, v] ** BETA))
        pesos = np.array(pesos); pesos /= pesos.sum()
        u, v = cand[rng.choice(len(cand), p=pesos)]
        arestas.append((u, v)); no_arvore.append(v)
    assert eh_arvore_valida(arestas)
    return arestas


def aco(seed=0):
    rng = np.random.default_rng(seed)
    tau = np.ones((N, N))
    melhor, melhor_c = None, np.inf
    hist = []
    for _ in range(N_ITER):
        formigas = [constroi_formiga(tau, rng) for _ in range(N_ANTS)]
        custos = np.array([custo(a) for a in formigas])
        ordem = np.argsort(custos)[:TOP_K]
        if custos[ordem[0]] < melhor_c:
            melhor_c, melhor = custos[ordem[0]], formigas[ordem[0]]
        # evaporacao (rho=0.2) + deposito apenas nas arestas das melhores topologias
        for idx in ordem:
            dep = Q / custos[idx]
            for i, j in formigas[idx]:
                tau[i, j] = tau[j, i] = (1 - RHO) * tau[i, j] + RHO * dep
        tau = np.clip(tau, TAU_MIN, TAU_MAX)
        hist.append(melhor_c)
    return melhor, melhor_c, np.array(hist)


def arvore_aleatoria(rng):
    nos = [int(rng.integers(N))]; arestas = []
    while len(nos) < N:
        u = nos[int(rng.integers(len(nos)))]
        restantes = [v for v in range(N) if v not in nos]
        v = restantes[int(rng.integers(len(restantes)))]
        arestas.append((u, v)); nos.append(v)
    return arestas


def mst_prim():
    nos = {0}; arestas = []
    while len(nos) < N:
        i, j = min(((i, j) for i in nos for j in range(N) if j not in nos), key=lambda e: D[e])
        arestas.append((i, j)); nos.add(j)
    return arestas


if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    print("Matriz de latencias D (ms):\n", D)
    arestas, c_aco, hist = aco(seed=1)
    adj = np.zeros((N, N), dtype=int)
    for i, j in arestas:
        adj[i, j] = adj[j, i] = 1
    print("\nMatriz de Adjacencia final (ACO):\n", adj)
    print("Arestas:", sorted(tuple(sorted(e)) for e in arestas))
    print("Valida (N-1 arestas, sem ciclos, conexa):", eh_arvore_valida(arestas))
    print("Latencia total das arestas (ms):", round(sum(D[i, j] for i, j in arestas), 1))
    print("Custo ACO (latencia ponderada dos pares criticos):", round(c_aco, 2))

    rng = np.random.default_rng(123)
    c_rand = np.array([custo(arvore_aleatoria(rng)) for _ in range(1000)])
    print(f"\nTopologia aleatoria (1000 amostras): media={c_rand.mean():.2f} desvio={c_rand.std():.2f} melhor={c_rand.min():.2f}")
    ganho_medio = 100 * (c_rand.mean() - c_aco) / c_rand.mean()
    print(f"Ganho do ACO vs aleatoria (media): {ganho_medio:.2f}%")
    c_mst = custo(mst_prim())
    print(f"Referencia MST (Prim): custo={c_mst:.2f} | ACO vs MST: {100*(c_mst-c_aco)/c_mst:.2f}%")

    custos_seeds = [aco(seed=s)[1] for s in range(10)]
    print(f"ACO em 10 sementes: media={np.mean(custos_seeds):.2f} desvio={np.std(custos_seeds):.2f} melhor={min(custos_seeds):.2f}")

    json.dump(dict(adj=adj.tolist(), arestas=[list(map(int, e)) for e in arestas], custo_aco=float(c_aco),
                   rand_media=float(c_rand.mean()), rand_std=float(c_rand.std()), ganho_medio=float(ganho_medio),
                   custo_mst=float(c_mst), seeds=[float(x) for x in custos_seeds], D=D.tolist()),
              open("lab03_results.json", "w"), indent=1)

    plt.figure(figsize=(8, 5))
    plt.plot(hist, label="ACO (melhor ate a iteracao)")
    plt.axhline(c_rand.mean(), color="tab:red", ls="--", label="Media aleatoria")
    plt.axhline(c_mst, color="tab:green", ls=":", label="MST (Prim)")
    plt.xlabel("Iteracao"); plt.ylabel("Custo (latencia ponderada, ms)")
    plt.title("Lab 03 - Convergencia do ACO"); plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig("lab03_convergencia.png", dpi=120)
