import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, skew
from pathlib import Path

out = Path(__file__).parent / "exponential_clt.png"

def sampling_dist(n, ax, rate=1.0, reps=10_000, seed=0):
    rng = np.random.default_rng(seed)
    mu_pop = sigma_pop = 1 / rate
    means = rng.exponential(1 / rate, size=(reps, n)).mean(axis=1)

    x = np.linspace(means.min(), means.max(), 500)
    ax.hist(means, bins=60, density=True, alpha=0.6)
    ax.plot(x, norm.pdf(x, loc=mu_pop, scale=sigma_pop / np.sqrt(n)), "g")
    ax.set_title(f"Exponential({rate}), n={n}")
    return means

n_values = [2, 5, 30]
fig, axes = plt.subplots(1, len(n_values), figsize=(5 * len(n_values), 4))
print(f"{'n':>4} {'mean':>8} {'std':>8} {'1/sqrt(n)':>10} {'skew':>8} {'2/sqrt(n)':>10}")
for n, ax in zip(n_values, axes):
    means = sampling_dist(n, ax)
    print(
        f"{n:>4} {means.mean():>8.3f} {means.std():>8.3f} {1/np.sqrt(n):>10.3f}"
        f" {skew(means):>8.3f} {2/np.sqrt(n):>10.3f}"
    )

fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)

for reps in [10_000, 100_000, 1_000_000]:
    gaps = []
    for seed in range(20):
        m = np.random.default_rng(seed).exponential(size=(reps, 5)).mean(axis=1)
        gaps.append(abs(skew(m) - 2/np.sqrt(5)))
    print(f"{reps:>9}  mean gap={np.mean(gaps):.4f}")
