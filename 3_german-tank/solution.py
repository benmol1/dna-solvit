
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


def print_results(N, results, N_est):
    print(f"mean:   {results.mean():.2f}")
    print(f"median: {np.median(results):.2f}")
    print(f"std:    {results.std():.2f}")
    print(f"true N: {N}")
    print()

    for key, estimates in N_est.items():
        bias = estimates.mean() - N
        rmse = np.sqrt(((estimates - N) ** 2).mean())
        print(f"{key:8s}  bias: {bias:8.2f}  rmse: {rmse:8.2f}")


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
    plt.yscale("log")
    plt.xlim(right=400)
    plt.grid(True, alpha=0.25)
    plt.xlabel("N")
    plt.ylabel("posterior probability")
    plt.title("Posterior distribution over N")
    plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def basic_simulation(k, N, num_sims, plot=False, save_path=None):
    serials = np.arange(N) + 1
    sample_means = []
    sample_maxima = []
    N_est = {}

    for sim in range(num_sims):
        sample = np.random.choice(serials, size=k, replace=False)
        sample_means.append(sample.mean())
        sample_maxima.append(sample.max())

    sample_means = np.array(sample_means)
    sample_maxima = np.array(sample_maxima)

    # one estimate per simulation (not an aggregate), so bias/rmse reflect
    # the spread of each estimator across repeated captures
    N_est["max"] = sample_maxima.astype(float)
    N_est["gaps"] = (k + 1) / k * sample_maxima - 1
    N_est["moments"] = 2 * sample_means - 1

    print_results(N, sample_maxima, N_est)
    if plot:
        plot_histogram(N, sample_maxima, save_path)


def baysian(observed_serials, N_max, plot=False, save_path=None):

    k = len(observed_serials)
    max_observed = np.array(observed_serials).max()

    # Initialise arrays
    N_values = np.arange(N_max) + 1
    prior = np.ones_like(N_values)
    probability_observed_serials = np.zeros_like(N_values, dtype=float)

    # Create a boolean mask for valid values of N (N can't possibly be less than k)
    valid = N_values >= k

    # Compute the likelyhood of the observed serials for each possible value of N
    probability_observed_serials[valid] = 1 / special.comb(N_values[valid], k)

    # Any value of N which is < max_observed is impossible (assuming that the tanks have sequential serial numbers!)
    probability_observed_serials[N_values < max_observed] = 0

    # Apply Bayes' rule
    unnormalized = prior * probability_observed_serials
    posterior = unnormalized / unnormalized.sum()

    # Find the median and 95% confidence interval of the N_values from the posterior distribution
    cumulative_posterior = np.cumsum(posterior)
    median = N_values[np.searchsorted(cumulative_posterior, 0.5)]
    q95_lower = N_values[np.searchsorted(cumulative_posterior, 0.025)]
    q95_upper = N_values[np.searchsorted(cumulative_posterior, 0.975)]
    print(f"posterior median: {median}")
    print(f"q95 interval: {q95_lower}-{q95_upper}")

    if plot:
        plot_posterior(N_values, posterior, median, q95_lower, q95_upper, save_path)


def main():
    k = 4
    N_true = 250
    num_sims = 100_000
    observed_serials = [19, 40, 42, 60]

    basic_simulation(
        k, N_true, num_sims, plot=True, save_path="3_german-tank/simulation.png"
    )
    baysian(
        observed_serials, N_max=1000, plot=True, save_path="3_german-tank/posterior.png"
    )


if __name__ == "__main__":
    main()
