#!/usr/bin/env python3
"""Mesh convergence study: k_eff and |error| vs mesh resolution.

Data are the results of running the solver at several cells-per-pin values.
Edit the arrays to match your own runs, then:
    python3 plot_convergence.py [out.png]
Requires only numpy + matplotlib.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = sys.argv[1] if len(sys.argv) > 1 else "mesh_convergence.png"

# ---- results per cells-per-pin (S(24x4), 20 threads) ----
cpp  = np.array([4, 6, 8, 10, 16])
keff = np.array([1.150391, 1.170711, 1.168785, 1.182204, 1.184733])
diff = np.array([-3615.9, -1583.9, -1776.5, -434.6, -181.7])   # pcm
kref = 1.18655

fig, ax = plt.subplots(1, 2, figsize=(13, 5))

a = ax[0]
a.axhline(kref, color="#5cb85c", lw=2, ls="--", label=f"NEA reference {kref}")
a.plot(cpp, keff, "o-", color="#d9534f", ms=8, lw=2, label="This solver (S$_N$)")
a.set_xlabel("Cells per pin (mesh resolution →)", fontsize=12)
a.set_ylabel("k$_{eff}$", fontsize=12)
a.set_title("k$_{eff}$ converges toward the reference\nas the mesh is refined", fontsize=12)
a.set_xticks(cpp); a.legend(fontsize=10); a.grid(alpha=0.3)

a = ax[1]
a.semilogy(cpp, np.abs(diff), "s-", color="#0275d8", ms=8, lw=2)
for x, y in zip(cpp, np.abs(diff)):
    a.annotate(f"{y:.0f}", (x, y), textcoords="offset points", xytext=(0, 8),
               fontsize=9, ha="center")
a.set_xlabel("Cells per pin (mesh resolution →)", fontsize=12)
a.set_ylabel("|k$_{eff}$ error|  [pcm]", fontsize=12)
a.set_title("Error drops from 3600 to 180 pcm\n(cpp=8 bump = stairstep effect)", fontsize=12)
a.set_xticks(cpp); a.grid(alpha=0.3, which="both")

fig.suptitle("C5G7 — Mesh Convergence Study (S$_N$ transport)", fontsize=14, weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(out, dpi=150)
print("wrote", out)
