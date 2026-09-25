from time import perf_counter

import numpy as np
from plotting import format_elapsed_time, plot_prob_k, plot_relative_simulation_error

NUM_SIMS = 100000
NUM_SEATS = 100
CUSTOMERS_WITH_NO_BOARDING_PASS = [1]
RUN_MODE = (
    "Error plot"  # Options: "Original only", "Optimized only", "Error plot", "Both"
)


def assign_random_seat(customer, seats, rng):
    available_seats = np.flatnonzero(seats == -1)
    if len(available_seats) == 0:
        raise ValueError("No available seats to assign.")
    seats[rng.choice(available_seats)] = customer


def run_simulations(num_sims, num_seats, customers_without_pass, rng):
    # Initialise results storage array
    results = np.zeros((num_sims, num_seats), dtype=bool)

    for simulation in range(num_sims):
        # Initialise seats array (-1 = unassigned)
        seats = np.full(num_seats, -1, dtype=int)

        for customer in range(1, num_seats + 1):
            assigned_seat = customer - 1

            # If the customer is without a boarding pass or their assigned seat is already taken,
            # assign a random available seat. Otherwise the customer gets their assigned seat.
            if customer in customers_without_pass or seats[assigned_seat] != -1:
                assign_random_seat(customer, seats, rng)
            else:
                seats[assigned_seat] = customer

        # The simulation is successful if the last customer (customer num_seats) gets their assigned seat
        results[simulation] = seats == np.arange(1, num_seats + 1)

    return results


def run_optimized_simulations(num_sims, num_seats, customers_without_pass, rng):
    if customers_without_pass != [1]:
        raise ValueError(
            "This optimized simulation expects customer 1 to lose their pass."
        )

    # The seat randomly assigned to customer 1 is the "displaced seat".
    displaced_seat = rng.integers(num_seats, size=num_sims)

    # Keep re-displacing until every simulation lands on an absorbing seat
    # (seat 0 = success, seat num_seats - 1 = failure).
    active = (displaced_seat != 0) & (displaced_seat != num_seats - 1)
    while np.any(active):
        active_idx = np.flatnonzero(active)
        current = displaced_seat[active_idx]

        # The number of remaining free seats depends on the displaced seat number.
        # The higher the displaced seat number, the fewer choices remain.
        random_rank = rng.integers(num_seats - current, size=len(active_idx))

        # Rank 0 means seat 0 was chosen; otherwise it's the seat that many places on.
        displaced_seat[active_idx] = np.where(
            random_rank == 0,
            0,
            current + random_rank,
        )

        active = (displaced_seat != 0) & (displaced_seat != num_seats - 1)

    results = displaced_seat == 0
    return results


def estimate_simulation_error(results) -> float:
    blocks = np.split(results, 10)
    block_means = np.mean(blocks, axis=1)
    return np.std(block_means)


def time_simulation(simulation_function, num_sims, num_seats, customers_without_pass):
    rng = np.random.default_rng()
    start_time = perf_counter()
    results = simulation_function(num_sims, num_seats, customers_without_pass, rng)
    elapsed_seconds = perf_counter() - start_time
    return results, elapsed_seconds


def main():
    print(f"Running {NUM_SIMS} simulations with {NUM_SEATS} seats...")
    print(f"Customers without boarding passes: {CUSTOMERS_WITH_NO_BOARDING_PASS}")

    def run(simulation_function):
        return time_simulation(
            simulation_function,
            NUM_SIMS,
            NUM_SEATS,
            CUSTOMERS_WITH_NO_BOARDING_PASS,
        )

    if RUN_MODE == "Optimized only":
        optimized_results, optimized_time = run(run_optimized_simulations)
        print(f"Optimized probability: {np.mean(optimized_results):.3f}")
        print(f"Optimized time: {format_elapsed_time(optimized_time)}")
        return

    if RUN_MODE == "Original only":
        original_results, original_time = run(run_simulations)

        prob_success = np.mean(original_results, axis=0)
        # sim_error = estimate_simulation_error(original_results)

        plot_prob_k(prob_success, NUM_SEATS)

        # print(f"Original simulation error: {sim_error:.3f} ({sim_error/prob_success:.1%})")
        print(f"Original time: {format_elapsed_time(original_time)}")

    if RUN_MODE == "Error plot":
        plot_relative_simulation_error(
            run_optimized_simulations,
            time_simulation,
            estimate_simulation_error,
            NUM_SEATS,
            CUSTOMERS_WITH_NO_BOARDING_PASS,
        )

    if RUN_MODE == "Both":
        original_results, original_time = run(run_simulations)
        optimized_results, optimized_time = run(run_optimized_simulations)

        print(f"Original probability: {np.mean(original_results[:, -1]):.3f}")
        print(f"Optimized probability: {np.mean(optimized_results):.3f}")
        print(f"Original time: {format_elapsed_time(original_time)}")
        print(f"Optimized time: {format_elapsed_time(optimized_time)}")
        print(
            f"Time ratio (original / optimized): {original_time / optimized_time:.1f}x"
        )


if __name__ == "__main__":
    main()
