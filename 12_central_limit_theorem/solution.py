from pathlib import Path
import numpy as np
from scipy.stats import norm, skew
import matplotlib.pyplot as plt


def sampling_dist(n, ax, rate=1.0, reps=10_000, seed=0):
    """Plot the sampling distribution of the mean of n Exponential(rate) draws.

    Draws `reps` samples of size n, histograms their means on `ax`, and overlays
    the CLT prediction N(mu, sigma / sqrt(n)), where mu = sigma = 1 / rate.
    Returns the array of sample means.
    """
    rng = np.random.default_rng(seed)
    mu_pop = sigma_pop = 1 / rate
    means = rng.exponential(1 / rate, size=(reps, n)).mean(axis=1)

    x = np.linspace(means.min(), means.max(), 500)
    ax.hist(means, bins=60, density=True, alpha=0.6)
    ax.plot(x, norm.pdf(x, loc=mu_pop, scale=sigma_pop / np.sqrt(n)), "g")
    ax.set_title(f"Exponential({rate}), n={n}")
    return means


def clt_exponential_dist():
    """Part 1: CLT for the skewed Exponential(1) distribution.

    Plots the sampling distribution of the mean for n = 2, 5, 30 with a normal
    overlay (saved to exponential_clt.png), and prints a table comparing the
    empirical mean, std and skew with the predictions 1/sqrt(n) and 2/sqrt(n).
    """
    out = Path(__file__).parent / "exponential_clt.png"
    n_values = [2, 5, 30]

    fig, axes = plt.subplots(1, len(n_values), figsize=(5 * len(n_values), 4))

    print(
        f"{'n':>4} {'mean':>8} {'std':>8} {'1/sqrt(n)':>10} {'skew':>8} {'2/sqrt(n)':>10}"
    )
    for n, ax in zip(n_values, axes):
        means = sampling_dist(n, ax)
        print(
            f"{n:>4} {means.mean():>8.3f} {means.std():>8.3f} {1 / np.sqrt(n):>10.3f}"
            f" {skew(means):>8.3f} {2 / np.sqrt(n):>10.3f}"
        )

    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def check_skew_exponential_dist():
    """Show that the skew prediction error shrinks like 1/sqrt(reps).

    For n = 5, prints the mean |empirical skew - 2/sqrt(5)| over 20 seeds at
    10k, 100k and 1M replications.
    """
    for reps in [10_000, 100_000, 1_000_000]:
        gaps = []
        for seed in range(20):
            m = np.random.default_rng(seed).exponential(size=(reps, 5)).mean(axis=1)
            gaps.append(abs(skew(m) - 2 / np.sqrt(5)))
        print(f"{reps:>9}  mean gap={np.mean(gaps):.4f}")


def running_sample_mean_cauchy_dist(n: int):
    """Part 2: plot the running mean of a single stream of n standard Cauchy draws.

    The running mean never settles, because Cauchy has no defined mean. Saved to
    cauchy_running_mean.png with a log-scaled x-axis.
    """
    rng = np.random.default_rng(seed=0)
    draws = rng.standard_cauchy(size=n)
    running_mean = np.cumsum(draws) / np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(np.arange(1, n + 1), running_mean, lw=0.8)
    ax.axhline(0, color="k", lw=0.5, ls="--")
    ax.set_xscale("log")
    ax.set_xlabel("number of draws")
    ax.set_ylabel("running mean")
    ax.set_title(f"Standard Cauchy: running mean over {n:,} draws")

    out = Path(__file__).parent / "cauchy_running_mean.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def uniform_convolution_test():
    """Show smoothing by repeated convolution of a Uniform(0, 1) density.

    The density of a sum of k independent variables is the k-fold convolution of
    their densities. Plots k = 1..4 (saved to uniform_convolution_test.png) to
    show a flat density becoming a triangle and then a bell shape.
    """
    dx = 0.001
    f = np.ones(int(1 / dx))  # uniform density on [0, 1]
    g = f.copy()
    fig, ax = plt.subplots(figsize=(8, 4))
    for k in range(1, 5):
        x = np.arange(len(g)) * dx
        ax.plot(x, g, label=f"sum of {k}")
        g = np.convolve(g, f) * dx
    ax.legend()

    out = Path(__file__).parent / "uniform_convolution_test.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    """Run the experiments; uncomment the ones you want to regenerate."""
    # clt_exponential_dist()
    # check_skew_exponential_dist()
    # running_sample_mean_cauchy_dist(1_000_000)
    uniform_convolution_test()


if __name__ == "__main__":
    main()
