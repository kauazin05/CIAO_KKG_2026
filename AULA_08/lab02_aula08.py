"""
LAB 02 - AG Binario com Penalidade para Selecao de Microsservicos em Edge (AULA 08)
Estrategia A: penalidade rigida (violou RAM ou CPU -> fitness = 0)
Estrategia B: penalidade proporcional ao excesso de RAM/CPU
"""
import itertools
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Tabela fixa de 15 microsservicos (premissa: o roteiro nao fornece os valores)
VALOR = np.array([60, 40, 90, 25, 70, 55, 30, 85, 45, 65, 20, 75, 50, 35, 80], dtype=float)
RAM = np.array([4.0, 2.0, 6.0, 1.0, 5.0, 3.0, 2.0, 7.0, 3.0, 4.0, 1.0, 5.0, 3.0, 2.0, 6.0])
CPU = np.array([2.0, 1.0, 3.0, 0.5, 2.0, 1.5, 1.0, 3.0, 1.0, 2.0, 0.5, 2.5, 1.5, 1.0, 2.5])
RAM_MAX, CPU_MAX = 16.0, 8.0
N = len(VALOR)
P_TOTAL = VALOR.sum()


def totais(ind):
    return ind @ VALOR, ind @ RAM, ind @ CPU


def viavel(ind):
    _, r, c = totais(ind)
    return r <= RAM_MAX and c <= CPU_MAX


def fit_A(ind):
    v, r, c = totais(ind)
    return 0.0 if (r > RAM_MAX or c > CPU_MAX) else v


def fit_B(ind):
    v, r, c = totais(ind)
    exc = max(0.0, r - RAM_MAX) / RAM_MAX + max(0.0, c - CPU_MAX) / CPU_MAX
    return max(0.0, v - P_TOTAL * exc)   # reducao proporcional ao excesso relativo


def diversidade(pop):
    """Distancia de Hamming media par a par, normalizada em [0,1]."""
    n = len(pop)
    d = (pop[:, None, :] != pop[None, :, :]).sum(axis=2)
    return d.sum() / (n * (n - 1) * pop.shape[1])


def ag(fit, seed, pop_size=60, gens=80, pc=0.85, pm=0.02, k=3, elite=1):
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, size=(pop_size, N)).astype(float)
    hist = dict(mean=[], std=[], div=[], feas=[])
    best_feas, best_feas_v = None, -1.0
    for _ in range(gens):
        f = np.array([fit(i) for i in pop])
        hist["mean"].append(f.mean()); hist["std"].append(f.std())
        hist["div"].append(diversidade(pop))
        hist["feas"].append(np.mean([viavel(i) for i in pop]))
        for ind in pop:
            if viavel(ind) and totais(ind)[0] > best_feas_v:
                best_feas_v, best_feas = totais(ind)[0], ind.copy()
        order = np.argsort(-f)
        new = [pop[i].copy() for i in order[:elite]]
        while len(new) < pop_size:
            def torneio():
                idx = rng.integers(0, pop_size, size=k)
                return pop[idx[np.argmax(f[idx])]]
            p1, p2 = torneio(), torneio()
            if rng.random() < pc:
                cut = rng.integers(1, N)
                c1 = np.concatenate([p1[:cut], p2[cut:]]); c2 = np.concatenate([p2[:cut], p1[cut:]])
            else:
                c1, c2 = p1.copy(), p2.copy()
            for c in (c1, c2):
                flip = rng.random(N) < pm
                c[flip] = 1 - c[flip]
                new.append(c)
        pop = np.array(new[:pop_size])
    return best_feas, best_feas_v, {k_: np.array(v) for k_, v in hist.items()}


def otimo_bruteforce():
    best, bv = None, -1
    for bits in itertools.product([0.0, 1.0], repeat=N):
        ind = np.array(bits)
        if viavel(ind) and totais(ind)[0] > bv:
            bv, best = totais(ind)[0], ind
    return best, bv


if __name__ == "__main__":
    opt, opt_v = otimo_bruteforce()
    print("Otimo global (forca bruta, 2^15):", opt_v, "servicos:", [i + 1 for i in np.flatnonzero(opt)])

    SEEDS = range(30)
    out = {}
    H = {}
    for nome, fit in (("A", fit_A), ("B", fit_B)):
        runs = [ag(fit, s) for s in SEEDS]
        H[nome] = {k: np.mean([r[2][k] for r in runs], axis=0) for k in ("mean", "std", "div", "feas")}
        vals = np.array([r[1] for r in runs])
        acertos = int(np.sum(vals == opt_v))
        b = runs[int(np.argmax(vals))][0]
        out[nome] = dict(melhor_media=float(vals.mean()), melhor_std=float(vals.std()),
                         acertos_otimo=acertos, melhor_valor=float(vals.max()),
                         servicos=[int(i + 1) for i in np.flatnonzero(b)],
                         ram=float(b @ RAM), cpu=float(b @ CPU),
                         div_inicial=float(H[nome]["div"][0]), div_final=float(H[nome]["div"][-1]),
                         div_media=float(H[nome]["div"].mean()),
                         feas_final=float(H[nome]["feas"][-1]))
        print(f"\nEstrategia {nome}: {out[nome]}")
    json.dump(dict(otimo=opt_v, resultados=out), open("lab02_results.json", "w"), indent=1)

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    g = np.arange(1, 81)
    for nome, cor in (("A", "tab:red"), ("B", "tab:blue")):
        ax[0].plot(g, H[nome]["mean"], color=cor, label=f"Estrategia {nome}")
        ax[0].fill_between(g, H[nome]["mean"] - H[nome]["std"], H[nome]["mean"] + H[nome]["std"], color=cor, alpha=.15)
        ax[1].plot(g, H[nome]["std"], color=cor, label=f"Estrategia {nome}")
        ax[2].plot(g, H[nome]["div"], color=cor, label=f"Estrategia {nome}")
    ax[0].set_title("Fitness medio (+/- desvio) por geracao"); ax[1].set_title("Desvio-padrao do fitness")
    ax[2].set_title("Diversidade genetica (Hamming medio)")
    for a in ax:
        a.set_xlabel("Geracao"); a.grid(alpha=.3); a.legend()
    plt.tight_layout(); plt.savefig("lab02_comparacao.png", dpi=120)
