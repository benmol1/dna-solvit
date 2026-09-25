import numpy as np


def format_elapsed_time(elapsed_seconds: float) -> str:
    if elapsed_seconds < 1e-3:
        return f"{elapsed_seconds * 1e6:.1f} µs"
    if elapsed_seconds < 1:
        return f"{elapsed_seconds * 1e3:.1f} ms"
    return f"{elapsed_seconds:.2f} s"


def prob_k_theory(num_seats):
    n = num_seats
    k = np.arange(1, n + 1)
    return np.where(k == 1, 1 / n, 1 - 1 / (n - k + 2))


def plot_prob_k(prob_k, num_seats):
    import matplotlib.pyplot as plt

    customer_numbers = np.arange(1, num_seats + 1)
    prob_k_theory_values = prob_k_theory(num_seats)

    plt.plot(
        customer_numbers,
        prob_k,
        marker="o",
        linestyle="None",
        label="Simulation",
    )

    plt.plot(
        customer_numbers,
        prob_k_theory_values,
        marker="None",
        linestyle="--",
        label="Theory: 1/n (k=1), 1 - 1/(n-k+2) (k>1)",
    )

    plt.xlabel("Customer number (k)")
    plt.ylabel("Probability of success")
    plt.title("Probability of success for k-th customer")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_relative_simulation_error(
    simulation_function,
    time_function,
    error_function,
    num_seats,
    customers_without_pass,
    min_sims=100,
    max_sims=1_000_000,
    num_points=15,
):
    import matplotlib.pyplot as plt

    simulation_counts = np.geomspace(min_sims, max_sims, num_points).astype(int)
    simulation_counts = np.unique((simulation_counts // 10) * 10)
    simulation_counts[0] = min_sims
    simulation_counts[-1] = max_sims
    relative_errors = []
    total_elapsed_seconds = 0.0

    for num_sims in simulation_counts:
        results, elapsed_seconds = time_function(
            simulation_function,
            num_sims,
            num_seats,
            customers_without_pass,
        )
        total_elapsed_seconds += elapsed_seconds
        probability = np.mean(results)
        simulation_error = error_function(results)
        relative_errors.append(simulation_error / probability)

    print(f"Total simulation time: {format_elapsed_time(total_elapsed_seconds)}")

    relative_errors = np.array(relative_errors)
    gradient, intercept = np.polyfit(
        np.log10(simulation_counts),
        np.log10(relative_errors),
        1,
    )
    fitted_errors = 10 ** (intercept + gradient * np.log10(simulation_counts))

    plt.plot(
        simulation_counts,
        relative_errors,
        marker="o",
        linestyle="None",
        label="Simulation",
    )
    plt.plot(
        simulation_counts,
        fitted_errors,
        linestyle="--",
        label=f"Power fit (exponent = {gradient:.3f})",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of simulations")
    plt.ylabel("Relative simulation error")
    plt.title("Relative simulation error and power-law fit")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return simulation_counts, relative_errors, gradient
