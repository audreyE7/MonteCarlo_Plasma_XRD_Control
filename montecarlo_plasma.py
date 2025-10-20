import json, csv
from pathlib import Path
import numpy as np

from xrd_model import temperature_proxy, hydrogenation_rate, oxidation_rate, phase_probabilities
from visualize_results import heatmap_current_pressure, convergence_plot, simple_sensitivity

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"

def sample(bounds, n, seed=0):
    rng = np.random.default_rng(seed)
    return {
        "current_A": rng.uniform(*bounds["current_A"], size=n),
        "pressure_Torr": rng.uniform(*bounds["pressure_Torr"], size=n),
        "h2_flow_sccm": rng.uniform(*bounds["h2_flow_sccm"], size=n),
        "exposure_s": rng.uniform(*bounds["exposure_s"], size=n),
        "oxygen_ppm": rng.uniform(*bounds["oxygen_ppm"], size=n),
    }

def run_mc(bounds):
    n = bounds.get("samples", 3000)
    seed = bounds.get("random_seed", 0)
    S = sample(bounds, n, seed)

    Tproxy = temperature_proxy(S["current_A"], S["pressure_Torr"], S["h2_flow_sccm"])
    k_h = hydrogenation_rate(Tproxy, S["h2_flow_sccm"], S["exposure_s"])
    k_o = oxidation_rate(Tproxy, S["oxygen_ppm"])
    p_h2, p_ox, p_mg = phase_probabilities(k_h, k_o)

    # Save CSV
    outcsv = RESULTS / "phase_probabilities.csv"
    outcsv.parent.mkdir(parents=True, exist_ok=True)
    with outcsv.open("w", newline="") as f:
        f.write("current_A,pressure_Torr,h2_flow_sccm,exposure_s,oxygen_ppm,P_MgH2,P_MgO,P_Mg\n")
        for i in range(n):
            f.write(f"{S['current_A'][i]},{S['pressure_Torr'][i]},{S['h2_flow_sccm'][i]},{S['exposure_s'][i]},{S['oxygen_ppm'][i]},{p_h2[i]},{p_ox[i]},{p_mg[i]}\n")

    # Heatmap vs current/pressure
    heatmap_current_pressure(S["current_A"], S["pressure_Torr"], p_h2, RESULTS/"phase_heatmap.png")

    # Convergence of mean P(MgH2)
    means = []
    step = max(1, n//50)
    for k in range(1000, n+1, step):
        means.append(p_h2[:k].mean())
    convergence_plot(np.array(means), RESULTS/"uncertainty_convergence.png")

    # Crude sensitivity: one-at-a-time ±10%
    base_mean = p_h2.mean()
    labels, pert = [], []
    for key, factor in [("current_A",1.1),("pressure_Torr",1.1),("h2_flow_sccm",1.1),("exposure_s",1.1),("oxygen_ppm",1.1)]:
        S2 = {k: v.copy() for k,v in S.items()}
        S2[key] = np.clip(S2[key]*factor, min(S2[key]), max(S2[key]))
        T2 = temperature_proxy(S2["current_A"], S2["pressure_Torr"], S2["h2_flow_sccm"])
        k_h2 = hydrogenation_rate(T2, S2["h2_flow_sccm"], S2["exposure_s"])
        k_o2 = oxidation_rate(T2, S2["oxygen_ppm"])
        p_h2b,_,_ = phase_probabilities(k_h2, k_o2)
        pert.append(p_h2b.mean())
        labels.append(key.replace("_"," "))
    import numpy as np
    simple_sensitivity(np.array([base_mean]*len(pert)), np.array(pert), labels, RESULTS/"sensitivity_radar.png")

    print(f"Saved {outcsv} and figures to {RESULTS}")

if __name__ == "__main__":
    bounds = json.loads((DATA/"plasma_bounds.json").read_text())
    run_mc(bounds)
