#!/usr/bin/env python3
"""Plot fast (g1) and thermal (g7) scalar flux maps from c5g7_flux.csv.

Usage:  python3 plot_flux.py [c5g7_flux.csv] [out.png]
Requires only numpy + matplotlib.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

csv = sys.argv[1] if len(sys.argv) > 1 else "c5g7_flux.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "flux_map.png"

d = np.genfromtxt(csv, delimiter=",", names=True)
n = int(round(np.sqrt(len(d))))
g1 = d["flux_g1"].reshape(n, n)
g7 = d["flux_g7"].reshape(n, n)
ext = [0, d["x_cm"].max(), 0, d["y_cm"].max()]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, data, title in [(axes[0], g1, "Fast flux  (group 1)"),
                        (axes[1], g7, "Thermal flux  (group 7)")]:
    im = ax.imshow(data, origin="lower", extent=ext, cmap="hot")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x [cm]"); ax.set_ylabel("y [cm]")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

fig.suptitle("C5G7 — Scalar Flux Distribution (S$_N$ transport)",
             fontsize=14, weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(out, dpi=150)
print("wrote", out)
