"""
xrd_model.py
------------
Toy kinetics + phase mapping for Mg ↔ MgH2 formation with oxidation competition.
"""
import numpy as np

def temperature_proxy(current_A, pressure_Torr, h2_flow_sccm):
    return (1.2*np.log1p(4*current_A) 
            + 0.8*np.log1p(3*pressure_Torr) 
            + 0.5*np.log1p(0.05*h2_flow_sccm))

def hydrogenation_rate(Tproxy, h2_flow_sccm, exposure_s):
    alpha = 0.35
    flow_term = np.log1p(0.06*h2_flow_sccm)
    time_term = np.log1p(exposure_s/60.0)
    return np.exp(alpha*Tproxy) * flow_term * time_term

def oxidation_rate(Tproxy, oxygen_ppm):
    beta = 0.22
    return np.exp(beta*Tproxy) * np.log1p(oxygen_ppm)

def phase_probabilities(k_hyd, k_ox):
    total = k_hyd + k_ox + 1.0
    p_mgh2 = k_hyd / total
    p_mgo  = k_ox  / total
    p_mg   = 1.0   / total
    s = p_mgh2 + p_mgo + p_mg
    return p_mgh2/s, p_mgo/s, p_mg/s
