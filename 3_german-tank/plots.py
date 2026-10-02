import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(N, results, save_path=None):
    plt.hist(results, bins=30, edgecolor="black")
    plt.axvline(N, color="red", linestyle="--", label=f"true N = {N}")
    plt.axvline(
        results.mean(),
        color="green",
        linestyle="--",
        label=f"mean max = {results.mean():.1f}",
    )
    plt.xlabel("max(sample)")
    plt.ylabel("count")
    plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_posterior(N_values, posterior, median, q95_lower, q95_upper, save_path=None):
    plt.plot(N_values, posterior)
    plt.axvline(median, color="red", linestyle="--", label=f"median = {median}")
    plt.axvspan(
        q95_lower,
        q95_upper,
        color="orange",
        alpha=0.2,
        label=f"95% CI = [{q95_lower}, {q95_upper}]",
    )
    plt.xlim(right=400)
    plt.grid(True, alpha=0.25)
    plt.xlabel("N")
    plt.ylabel("posterior probability")
    plt.title("Posterior distribution over N")
    plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_prior_sd_sweep(
    N_values, uniform_posterior, uniform_median, sweep, prior_mean, save_path=None
):
    """Plot posteriors over N for a flat prior and a list of normal-prior SDs.

    `sweep` is a list of (sd, posterior, median) tuples.
    """
    fig, ax = plt.subplots()

    ax.plot(
        N_values,
        uniform_posterior,
        color="black",
        linestyle="--",
        label=f"uniform prior (median = {uniform_median})",
    )

    colors = plt.cm.rainbow(np.linspace(0, 1, len(sweep)))
    for (sd, posterior, median), color in zip(sweep, colors):
        ax.plot(
            N_values, posterior, color=color, label=f"SD = {sd} (median = {median})"
        )

    ax.set_xlim(right=400)
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("N")
    ax.set_ylabel("posterior probability")
    ax.set_title(f"Posterior over N by prior SD (normal prior, mean = {prior_mean})")
    ax.legend()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
