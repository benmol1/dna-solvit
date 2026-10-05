import numpy as np
from scipy import special
from scipy.stats import norm

import plots


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
        plots.plot_histogram(N, sample_maxima, save_path)


def baysian(
    observed_serials,
    prior_shape="uniform",
    prior_mean=100,
    prior_sd=20,
    N_max=1000,
    plot=False,
    save_path=None,
    verbose=True,
):

    k = len(observed_serials)
    max_observed = np.array(observed_serials).max()

    # Initialise arrays
    N_values = np.arange(N_max) + 1
    probability_observed_serials = np.zeros_like(N_values, dtype=float)
    if prior_shape == "uniform":
        prior = np.ones_like(N_values)
    elif prior_shape == "normal":
        prior = norm.pdf(N_values, loc=prior_mean, scale=prior_sd)

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
    if verbose:
        print(f"posterior median: {median}")
        print(f"q95 interval: {q95_lower}-{q95_upper}")

    if plot:
        plots.plot_posterior(
            N_values, posterior, median, q95_lower, q95_upper, save_path
        )

    return N_values, posterior, median


def prior_sd_sweep(observed_serials, sds, prior_mean=100, N_max=1000, save_path=None):
    """Compute posteriors over N for a flat prior and a range of normal-prior SDs."""
    N_values, uniform_posterior, uniform_median = baysian(
        observed_serials, prior_shape="uniform", N_max=N_max, verbose=False
    )

    sweep = []
    for sd in sds:
        _, posterior, median = baysian(
            observed_serials,
            prior_shape="normal",
            prior_mean=prior_mean,
            prior_sd=sd,
            N_max=N_max,
            verbose=False,
        )
        sweep.append((sd, posterior, median))

    plots.plot_prior_sd_sweep(
        N_values, uniform_posterior, uniform_median, sweep, prior_mean, save_path
    )


def main():
    k = 4
    N_true = 250
    num_sims = 100_000
    observed_serials = [19, 40, 42, 60]

    # basic_simulation(
    #     k, N_true, num_sims, plot=True, save_path="3_german-tank/simulation.png"
    # )
    # baysian(
    #     observed_serials, N_max=1000, prior_shape="normal", plot=True
    # )
    prior_sd_sweep(
        observed_serials,
        sds=[5, 10, 20, 50, 100, 500],
        save_path="3_german-tank/prior_sd_sweep.png",
    )


if __name__ == "__main__":
    main()
