# MonteCarlo_Plasma_XRD_Control

Quantify how **plasma parameter uncertainty** (current, pressure, H₂ flow, exposure time) propagates to **phase outcomes** visible in **XRD**.

This scaffold provides:
- A **Monte Carlo sampler** for plasma control variables
- A **simple reaction/phase model** (Arrhenius-style hydrogenation + oxidation competition)
- **Phase probability estimates** (Mg, MgH₂, MgO)
- **Plots** and saved CSVs for quick iteration

> Replace `xrd_model.py` with your lab-specific kinetics once you have data. The defaults are deliberately simple but physically plausible.

---

## Quick start

```bash
# run everything and generate figures into /results
python src/montecarlo_plasma.py
```

Artifacts:
- `results/phase_probabilities.csv` — per-sample phase probabilities
- `results/phase_heatmap.png` — P(MgH₂) vs current and pressure
- `results/sensitivity_radar.png` — crude one-at-a-time sensitivity (normalized)
- `results/uncertainty_convergence.png` — MC convergence of mean P(MgH₂)

---

## Files

```
src/
  montecarlo_plasma.py   # runs simulation end-to-end
  xrd_model.py           # simple kinetics + phase mapping
  visualize_results.py   # plotting utilities
data/
  plasma_bounds.json     # editable parameter ranges
results/
  (generated outputs)
```

---

## Editable parameter ranges

Edit `data/plasma_bounds.json` to match your tool. Units noted inline.

- current [A]
- pressure [Torr]
- h2_flow [sccm]
- exposure [s]
- oxygen_ppm [ppm] (background leak / contamination)

---

## Notes

- No proprietary data. Synthetic, portfolio-safe defaults.
- All plots use **matplotlib** with default styles (no seaborn).
- Keep units consistent if you modify bounds or the model.
