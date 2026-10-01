import numpy as np
import matplotlib.pyplot as plt


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


def plot_histogram(N, results):
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
    plt.show()


def basic_simulation(k, N, num_sims):
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
    # plot_histogram(N, results)


# TODO: Bayesian extension — put a uniform prior on N (60..1000), compute
# the posterior over N given the captured serials (19, 40, 42, 60), report
# a 95% credible interval, and compare the posterior median to 74.


def main():
    k = 4
    N = 250
    num_sims = 100_000

    basic_simulation(k, N, num_sims)


if __name__ == "__main__":
    main()
