import random
from pathlib import Path

import matplotlib.pyplot as plt

weights = [4, 11, 25, 14, 29, 29, 8, 29, 1, 3, 16, 1, 11, 14, 10, 28, 9, 25, 18, 28, 21, 25, 29, 5, 15]  # fmt: skip
values = [59, 45, 22, 40, 1, 53, 3, 32, 2, 46, 35, 24, 35, 23, 7, 2, 41, 40, 10, 21, 25, 6, 21, 12, 52]  # fmt: skip
CAPACITY = 100

order = sorted(range(25), key=lambda i: values[i] / weights[i], reverse=True)


def knapsack_greedy(weights, values, capacity):
    """Pack the bag in descending order of value density. No swaps."""
    total_w = total_v = item_count = 0
    for i in order:
        if total_w + weights[i] <= capacity:
            total_w += weights[i]
            total_v += values[i]
            item_count += 1
    return (total_v, total_w, item_count)


def knapsack_dp(weights, values, capacity):
    """Return the best total value achievable within capacity."""
    best = [0] * (capacity + 1)

    # Loop over the weight:value pairs in the item list
    for w, v in zip(weights, values):
        best_new = best.copy()

        # Loop over all capacities
        for c in range(1, capacity + 1):
            # If the capacity can accomodate the weight of the current item
            # check which is better: the previous best at this capacity (leave this item out),
            # or the best at capacity c-w + the value of the item (put this item in)
            if c >= w:
                best_new[c] = max(best[c], best[c - w] + v)
        best = best_new

    # best[c] is the maximum possible knapsack value for a given capacity c
    return best[capacity]


def random_subset_test():
    import random

    weights = [4, 11, 25, 14, 29, 29, 8, 29, 1, 3, 16, 1, 11, 14, 10, 28, 9, 25, 18, 28, 21, 25, 29, 5, 15]  # fmt: skip

    trials = 100_000
    ok = sum(
        sum(w for w in weights if random.random() < 0.5) <= 100 for _ in range(trials)
    )
    print(ok / trials)


def fitness_linear(bits, alpha):
    w = sum(b * wi for b, wi in zip(bits, weights))
    v = sum(b * vi for b, vi in zip(bits, values))
    return v - alpha * max(0, w - CAPACITY)


def plot_fitness_histogram(fits, filename="fitness_hist.png", title=None):
    """Save a histogram of the fitness values to a PNG next to this file."""
    fig, ax = plt.subplots()
    ax.hist(fits, bins=30)
    ax.axvline(0, color="grey", linestyle=":")
    ax.set_xlabel("fitness")
    ax.set_ylabel("number of individuals")
    ax.set_title(title or f"Fitness of {len(fits)} individuals")
    path = Path(__file__).parent / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def print_value_density():
    dens = [v / w for v, w in zip(values, weights)]
    print(f"value per kg: min {min(dens):.2f}, max {max(dens):.2f}")


def tournament(pop, fits, k=2):
    picks = random.sample(range(len(pop)), k)
    return pop[max(picks, key=lambda i: fits[i])]


def crossover(p1, p2, cutoff=13):
    child = p1[:cutoff] + p2[cutoff:]
    return child


def mutate(bits, rate=1 / 25):
    """Return a new list with each bit flipped independently with probability rate."""
    return [1 - b if random.random() < rate else b for b in bits]


def make_child(pop, fits, k, rate, use_crossover=True):
    p1 = tournament(pop, fits, k)
    if use_crossover:
        p2 = tournament(pop, fits, k)
        child = crossover(p1, p2)  # TODO: random cutoff
    else:
        child = p1.copy()
    return mutate(child, rate)


def run_ga(
    alpha,
    k=2,
    rate=1 / 25,
    pop_size=100,
    generations=200,
    n_elite=2,
    use_crossover=True,
):
    pop = [[random.randint(0, 1) for _ in range(25)] for _ in range(pop_size)]
    best_hist, mean_hist = [], []

    for gen in range(generations):
        fits = [fitness_linear(ind, alpha) for ind in pop]
        best_hist.append(max(fits))
        mean_hist.append(sum(fits) / len(fits))

        # 1. elites: the n_elite best individuals, copied unchanged
        ranked = sorted(range(pop_size), key=lambda i: fits[i], reverse=True)
        new_pop = [pop[i].copy() for i in ranked[:n_elite]]
        # 2. fill the rest of the next generation with make_child(...)
        for _ in range(pop_size - n_elite):
            new_pop.append(make_child(pop, fits, k, rate, use_crossover))
        pop = new_pop

    return best_hist, mean_hist


def main():
    # greedy = knapsack_greedy(weights, values, CAPACITY)
    # print(f"total_value: {greedy[0]}, total_weight: {greedy[1]}, item_count: {greedy[2]}")

    # random_subset_test()

    # answer = knapsack_dp(weights, values, CAPACITY)
    # print(answer)

    num_items = len(values)
    alpha = 2
    pop = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(100)]

    fits = [fitness_linear(ind, alpha) for ind in pop]
    plot_fitness_histogram(
        fits,
        filename=f"fitness_hist_alpha={alpha}.png",
        title=f"Random population, alpha={alpha}",
    )

    winner = tournament(pop, fits, 2)
    print(f"winner: {winner}")

    print(crossover([1] * 25, [0] * 25, 10))


if __name__ == "__main__":
    main()
