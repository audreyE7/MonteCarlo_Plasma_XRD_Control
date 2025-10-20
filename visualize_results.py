import numpy as np
import matplotlib.pyplot as plt

def heatmap_current_pressure(currents, pressures, p_mgh2, outpath):
    nb = 24
    H, xedges, yedges = np.histogram2d(currents, pressures, bins=nb, weights=p_mgh2)
    N, _, _ = np.histogram2d(currents, pressures, bins=nb)
    with np.errstate(invalid='ignore'):
        Z = np.divide(H, N, where=N>0)
    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    im = ax.imshow(Z.T, origin='lower', aspect='auto',
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    cbar = plt.colorbar(im, ax=ax)
    ax.set_xlabel("Current [A]")
    ax.set_ylabel("Pressure [Torr]")
    cbar.set_label("Mean P(MgH2)")
    plt.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)

def convergence_plot(means, outpath):
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(np.arange(1, len(means)+1), means)
    ax.set_xlabel("Samples (k)")
    ax.set_ylabel("Mean P(MgH2)")
    ax.set_title("Monte Carlo Convergence")
    plt.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)

def simple_sensitivity(baseline, perturbed, labels, outpath):
    delta = np.abs(perturbed - baseline)
    if delta.max() > 0:
        delta = delta / delta.max()
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.bar(labels, delta)
    ax.set_ylabel("Normalized sensitivity")
    plt.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)
