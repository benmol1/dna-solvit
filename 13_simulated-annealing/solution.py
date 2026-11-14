import random
import math
import time
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent


def two_opt(tour, i, j):
    """Return a new tour with positions i..j (inclusive) reversed."""
    return tour[:i] + tour[i:j+1][::-1] + tour[j+1:]


def get_original_cities():
    """Return the 12 cities from the original problem statement."""
    return [(77,44),(86,70),(9,98),(76,79),(13,45),(37,93),
            (64,82),(44,23),(55,6),(83,63),(76,35),(97,89)]


def random_cities(n, size=100, seed=None):
    """Return n random (x, y) integer points in a size x size square.

    Pass a seed to get the same cities every time, which makes comparing
    runs and cooling schedules fair.
    """
    rng = random.Random(seed)
    return [(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)]


def city_distance(city_a, city_b):
    """Return the Euclidean distance between two (x, y) points."""
    (x1, y1), (x2, y2) = city_a, city_b
    return math.hypot(x2 - x1, y2 - y1)


class TSP:
    """A travelling-salesman instance: the cities plus everything that depends on them.

    A tour is a list of indices into cities, in visiting order. The distances
    between all pairs of cities are precomputed once, so evaluating a move is
    just a few table lookups.
    """

    def __init__(self, cities):
        """Store the cities and precompute the full pairwise distance matrix."""
        self.cities = cities
        self.n = len(cities)
        self.dist = [[city_distance(a, b) for b in cities] for a in cities]

    def random_tour(self):
        """Return a uniformly random tour of all cities."""
        return random.sample(range(self.n), self.n)

    def tour_length(self, tour):
        """Return the length of the closed tour, including the edge back to the start."""
        return sum(self.dist[tour[ii-1]][tour[ii]] for ii in range(len(tour)))

    def two_opt_delta(self, tour, i, j):
        """Return the change in tour length if positions i..j were reversed (i < j).

        Only the two boundary edges change: (a, b) and (c, d) are replaced by
        (a, c) and (b, d), so this is O(1) rather than recomputing the whole tour.
        Negative means the move shortens the tour. Indices wrap around the loop.
        """
        n = len(tour)

        # Guard for the case of the whole tour being reversed
        if abs(i-j) == n-1:
            return 0

        a, b = tour[i-1], tour[i]
        c, d = tour[j], tour[(j+1) % n]

        return self.dist[a][c] + self.dist[b][d] - self.dist[a][b] - self.dist[c][d]

    def hill_climb(self, tour):
        """Apply the best improving 2-opt move until none remains; return the tour."""
        n = len(tour)

        while True:
            # 1. scan all i < j, tracking the most negative delta and its (i, j)
            best_i, best_j = -1, -1
            best_delta = -1e-9  # tolerance: ignore floating-point noise
            for jj in range(n):
                for ii in range(jj):
                    delta = self.two_opt_delta(tour, ii, jj)
                    if delta < best_delta:
                        best_delta = delta
                        best_i, best_j = ii, jj
            # 2. no improving move found: this is a local optimum
            if best_i == -1:
                break
            # 3. otherwise apply the best move
            tour = two_opt(tour, best_i, best_j)
        return tour

    def annealing(self, tour, T0=5, cooling=1-3e-5, steps=50_000, trace=None):
        """Simulated annealing with random 2-opt moves and geometric cooling.

        A move with change delta is accepted if delta < 0, else with probability
        exp(-delta / T). T starts at T0 and is multiplied by cooling every step.

        Returns the shortest tour visited (not necessarily the final one). If
        trace is a list, the current tour length after each step is appended to
        it, for plotting.
        """
        T = T0
        current = self.tour_length(tour)
        best_tour, best_length = tour, current

        for _ in range(steps):
            i, j = sorted(random.sample(range(self.n), 2))
            delta = self.two_opt_delta(tour, i, j)

            if delta < 0 or random.random() < math.exp(-delta / T):
                tour = two_opt(tour, i, j)
                current += delta
                if current < best_length:
                    best_tour, best_length = tour, current

            if trace is not None:
                trace.append(current)
            T *= cooling

        return best_tour

    def plot_tour(self, tour, title=None, ax=None):
        """Draw a closed tour over the cities, numbering each stop.

        The start city is red. Draws on ax if given, else a new figure, and returns the axes.
        """
        cities = self.cities
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 6))

        xs = [cities[i][0] for i in tour] + [cities[tour[0]][0]]
        ys = [cities[i][1] for i in tour] + [cities[tour[0]][1]]

        ax.plot(xs, ys, "-o", color="tab:blue", markersize=6)
        for step, city in enumerate(tour):
            ax.annotate(step, cities[city], textcoords="offset points", xytext=(5, 5))
        ax.plot(*cities[tour[0]], "o", color="tab:red", markersize=10)  # start city

        ax.set_title(title or f"Tour length = {self.tour_length(tour):.2f}")
        ax.set_aspect("equal")
        return ax

    def check_two_opt_delta(self, tour):
        """Assert two_opt_delta matches a brute-force length difference for every i < j."""
        n = len(tour)

        for jj in range(n):
            for ii in range(jj):
                clever = self.two_opt_delta(tour, ii, jj)
                simple = self.tour_length(two_opt(tour, ii, jj)) - self.tour_length(tour)
                assert math.isclose(clever, simple, abs_tol=1e-6), (tour, ii, jj, clever, simple)


def plot_histogram(results, filename, title, optimum=None, bins=30):
    """Save overlaid histograms of final tour lengths to OUT_DIR/filename.

    results maps a label (e.g. "Hill climbing") to its list of lengths. All
    series share the same bins so they can be compared directly. The optimum,
    if known, is marked with a dashed line.
    """
    fig, ax = plt.subplots(figsize=(7, 4))

    edges = np.histogram_bin_edges(np.concatenate(list(results.values())), bins=bins)
    for label, lengths in results.items():
        ax.hist(lengths, bins=edges, alpha=0.6, edgecolor="white", label=label)
    if optimum is not None:
        ax.axvline(optimum, color="tab:red", linestyle="--", label=f"optimum {optimum}")

    ax.set_xlabel("Final tour length")
    ax.set_ylabel("Number of runs")
    ax.set_title(title)
    ax.legend()

    fig.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_tour(problem, tour, filename, title=None):
    """Plot a tour on the given TSP instance and save it to OUT_DIR/filename."""
    problem.plot_tour(tour, title=title)
    plt.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close()


def plot_trace(trace, T0, cooling, filename):
    """Save the tour length over time, with the temperature schedule beneath it.

    trace is the current length after each annealing step. The temperature is
    rebuilt from the schedule (T0 * cooling**step). Both panels share the step
    axis so you can see which temperature regime each part of the trace is in.
    """
    steps = np.arange(len(trace))
    temperature = T0 * cooling ** steps

    fig, (ax_len, ax_temp) = plt.subplots(2, 1, sharex=True, figsize=(8, 6),
                                          gridspec_kw={"height_ratios": [3, 1]})
    ax_len.plot(steps, trace, linewidth=0.6)
    ax_len.set_yscale("log")
    ax_len.set_ylabel("Current tour length (log scale)")
    ax_len.set_title(f"Annealing trace: start {trace[0]:.0f}, end {trace[-1]:.1f}")

    ax_temp.plot(steps, temperature, color="tab:red")
    ax_temp.set_yscale("log")
    ax_temp.set_ylabel("Temperature T")
    ax_temp.set_xlabel("Step")

    fig.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def run_restarts(problem, solver, n_trials):
    """Run solver (tour -> final tour) from n_trials random starts.

    Returns (lengths, best_tour, seconds): the final length of each run, the
    shortest tour found, and the total wall-clock time.
    """
    start = time.perf_counter()
    lengths, best_tour, best_length = [], None, math.inf
    for _ in range(n_trials):
        final_tour = solver(problem.random_tour())
        final_length = problem.tour_length(final_tour)
        lengths.append(final_length)
        if final_length < best_length:
            best_tour, best_length = final_tour, final_length
    return lengths, best_tour, time.perf_counter() - start


def print_stats(label, lengths, seconds):
    """Print summary statistics for one method's final tour lengths."""
    arr = np.array(lengths)
    print(f"{label:<14} min: {arr.min():.2f}  max: {arr.max():.2f}  mean: {arr.mean():.2f}  "
          f"median: {np.median(arr):.2f}  stdev: {arr.std():.2f}  time: {seconds:.1f}s")


def main():
    """Compare hill climbing with annealing on 50 cities and plot an annealing trace."""

    n_trials = 20
    schedule = dict(T0=5, cooling=1 - 3e-5, steps=50_000)

    small = TSP(get_original_cities())
    big = TSP(random_cities(n=50, seed=2))

    methods = {
        "Hill climbing": big.hill_climb,
        "Annealing": partial(big.annealing, **schedule),
    }

    results, best_tours = {}, {}
    for label, solver in methods.items():
        lengths, best_tour, seconds = run_restarts(big, solver, n_trials)
        results[label], best_tours[label] = lengths, best_tour
        print_stats(label, lengths, seconds)

    plot_histogram(results, "comparison_hist.png",
                   title=f"Final tour length, {n_trials} restarts each (50 cities)")
    for label, tour in best_tours.items():
        filename = f"best_{label.lower().replace(' ', '_')}_tour.png"
        plot_tour(big, tour, filename, title=f"Best {label.lower()} tour: {big.tour_length(tour):.2f}")

    # One annealing run with its length recorded at every step
    trace = []
    big.annealing(big.random_tour(), trace=trace, **schedule)
    plot_trace(trace, schedule["T0"], schedule["cooling"], "annealing_trace.png")


if __name__ == "__main__":
    main()
