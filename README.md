# Steady-State Heat Conduction in a TRISO Particle

A combined **3D CFD (Star-CCM+)** and **1D analytical** study of steady-state heat
conduction inside a single multi-layer **TRISO** (Tristructural-Isotropic) nuclear
fuel particle.

> NEM 358 — Computational Fluid Dynamics Applications · Hacettepe University, Department of Nuclear Engineering.

---

## Problem Description

TRISO particles are designed to withstand extreme temperatures and radiation
thanks to their multilayer structure. This project models the steady-state
temperature distribution within a single particle consisting of five concentric
regions:

1. **UO₂ fuel kernel** — internal volumetric heat generation of `2 GW/m³`
2. **Porous carbon buffer**
3. **Inner pyrolytic carbon (IPyC)**
4. **Silicon carbide (SiC)**
5. **Outer pyrolytic carbon (OPyC)**

Heat is generated only in the kernel and transferred outward purely by
**conduction** (no contact resistance, isotropic properties). The outer surface
is held at a fixed temperature of `1073.15 K`.

---

## Methodology

### Governing Equations
Steady-state heat conduction in spherical coordinates:

- Non-generating shells (regions 2–5):  `(1/r²) d/dr (r² dT/dr) = 0`
- Fuel kernel (region 1):               `(1/r²) d/dr (r² dT/dr) + q̇/k₁ = 0`

### Analytical Solution (1D radial)
The peak centre temperature is obtained by summing the parabolic rise in the
kernel and the conductive drop across each shell:

```
T_max = T_s + Σ ΔT_i + q̇·r₁² / (6·k₁)
```

with the shell drops given by the spherical thermal-resistance relation
`ΔT_i = Q/(4πk_i)·(1/r_in − 1/r_out)`.

### Numerical Setup (Star-CCM+)
- 3D spherical model, 5 concentric regions, polyhedral mesh
- Segregated Fluid Temperature, Steady-State solver
- Fixed outer-surface temperature `1073.15 K`
- Three mesh levels for the independence study: Coarse `0.04 mm`, Medium `0.02 mm`, Fine `0.01 mm`

---

## Key Results

| Case | h (mm) | Cells (N) | T_max (K) | Error vs analytical |
| :--- | :--- | :--- | :--- | :--- |
| Coarse | 0.04 | 90,145 | 1106.443 | 0.0084 % |
| Medium | 0.02 | 101,239 | 1106.129 | 0.0200 % |
| Fine | 0.01 | 452,282 | 1105.440 | 0.0823 % |
| Bonus `k(T)` | 0.01 | 452,282 | 1104.896 | 0.1314 % |
| **Analytical** | — | — | **1106.350** | — |

* **Mesh independence proven:** the maximum deviation from the analytical
  reference (`1106.35 K`) stays **below 1 K** at every mesh level, with relative
  errors well under the 0.1 % tolerance.
* Refining the mesh beyond the medium level does **not** meaningfully improve
  accuracy — it only increases computational cost.
* A bonus case incorporating **temperature-dependent UO₂ conductivity `k(T)`**
  was compared against the constant-conductivity assumption.

---

## Contents

- `triso-heat-conduction-cfd.pdf` — full project report (methodology, results, analytical derivation).

## Author

**Emre Sakarya** — Nuclear Engineering, Hacettepe University (Student ID: 2230386062).
