#!/usr/bin/env python3
"""Plot the normalised pin power distribution from c5g7_pinpower.csv.

Usage:  python3 plot_pinpower.py [c5g7_pinpower.csv] [out.png]
Requires only numpy + matplotlib.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

csv = sys.argv[1] if len(sys.argv) > 1 else "c5g7_pinpower.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "pinpower_map.png"

d = np.genfromtxt(csv, delimiter=",", names=True)
pc = d["pc"].astype(int); pr = d["pr"].astype(int); val = d["norm_power"]

pc0, pc1 = pc.min(), pc.max()
pr0, pr1 = pr.min(), pr.max()
ncol, nrow = pc1 - pc0 + 1, pr1 - pr0 + 1
grid = np.full((nrow, ncol), np.nan)
grid[pr - pr0, pc - pc0] = val

fuel = val[val > 0.05]
print(f"max = {fuel.max():.4f}  min = {fuel.min():.4f}  (ref 2.498 / 0.232)")

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(grid, origin="lower", cmap="jet", vmin=0, vmax=2.4)
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Normalised pin power", fontsize=12)

ax.axhline(nrow / 2 - 0.5, color="k", lw=1.2)
ax.axvline(ncol / 2 - 0.5, color="k", lw=1.2)

q = ncol / 4
for (xx, yy, lab) in [(q, nrow * 0.75, "UO$_2$"), (3 * q, nrow * 0.75, "MOX"),
                      (q, nrow * 0.25, "MOX"), (3 * q, nrow * 0.25, "UO$_2$")]:
    ax.text(xx, yy, lab, ha="center", va="center",
            fontsize=14, color="white", weight="bold")

ax.set_xlabel("Pin column")
ax.set_ylabel("Pin row")
ax.set_title("C5G7 — Normalised Pin Power Distribution (S$_N$ transport)")
plt.tight_layout()
plt.savefig(out, dpi=150)
print("wrote", out)
