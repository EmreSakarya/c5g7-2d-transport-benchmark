#!/usr/bin/env python3
"""Scalar benchmark comparison: this S_N solver vs the OECD/NEA reference.

Edit the values below to match your run, then:
    python3 plot_benchmark.py [out.png]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = sys.argv[1] if len(sys.argv) > 1 else "benchmark_compare.png"

# ---- results (cpp=16, S(24x4), 20 threads) ----
keff_ours, keff_ref = 1.184733, 1.186550
pin_ours = [2.3529, 0.2182]      # max, min
pin_ref  = [2.498, 0.232]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# panel 1: k_eff
ax = axes[0]
bars = ax.bar(["This solver\n(S$_N$ transport)", "NEA reference\n(MCNP)"],
              [keff_ours, keff_ref], color=["#d9534f", "#5cb85c"],
              width=0.55, edgecolor="k")
ax.set_ylim(1.180, 1.190)
ax.set_ylabel("k$_{eff}$", fontsize=13)
dpcm = (keff_ours - keff_ref) * 1e5
ax.set_title(f"Effective multiplication factor  ({dpcm:+.0f} pcm)", fontsize=12)
for b, v in zip(bars, [keff_ours, keff_ref]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.0002, f"{v:.5f}",
            ha="center", fontsize=12, weight="bold")
ax.grid(axis="y", alpha=0.3)

# panel 2: pin power extremes
ax = axes[1]
x = np.arange(2); w = 0.36
b1 = ax.bar(x - w / 2, pin_ours, w, label="This solver", color="#d9534f", edgecolor="k")
b2 = ax.bar(x + w / 2, pin_ref,  w, label="NEA reference", color="#5cb85c", edgecolor="k")
ax.set_xticks(x); ax.set_xticklabels(["Max pin power", "Min pin power"], fontsize=11)
ax.set_ylabel("Normalised pin power", fontsize=13)
ax.set_title("Pin power extremes  (both $\\approx$6 % low)", fontsize=12)
ax.legend(fontsize=11)
for bars, vals in [(b1, pin_ours), (b2, pin_ref)]:
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.03, f"{v:.3f}",
                ha="center", fontsize=10)
ax.grid(axis="y", alpha=0.3)

fig.suptitle("C5G7 2-D Benchmark — This S$_N$ Solver vs OECD/NEA Reference",
             fontsize=14, weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(out, dpi=150)
print("wrote", out)
