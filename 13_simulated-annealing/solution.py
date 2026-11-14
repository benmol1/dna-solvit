import random
import math
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


def plot_histogram(lengths, filename="hill_climb_hist.png", optimum=None, bins=30):
    """Save a histogram of tour lengths to OUT_DIR/filename, marking the optimum if known."""
    fig, ax = plt.subplots(figsize=(7, 4))

    ax.hist(lengths, bins=bins, color="tab:blue", edgecolor="white")
    if optimum is not None:
        ax.axvline(optimum, color="tab:red", linestyle="--", label=f"optimum {optimum}")
        ax.legend()

    ax.set_xlabel("Final tour length")
    ax.set_ylabel("Number of runs")
    ax.set_title(f"Hill climbing local optima ({len(lengths)} restarts)")

    fig.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_tour(problem, tour, filename, title=None):
    """Plot a tour on the given TSP instance and save it to OUT_DIR/filename."""
    problem.plot_tour(tour, title=title)
    plt.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    """Check the delta calculation, then run hill-climbing restarts on 50 random cities."""

    verbose = False
    n_trials = 100

    small = TSP(get_original_cities())
    big = TSP(random_cities(n=50, seed=1))

    # Refactor safety net: the O(1) delta must agree with brute force on both instances.
    for problem in (small, big):
        for _ in range(20):
            problem.check_two_opt_delta(problem.random_tour())

    lengths = []
    best_tour = None
    for _ in range(n_trials):
        tour = big.random_tour()
        final_tour = big.hill_climb(tour)
        final_length = big.tour_length(final_tour)
        if verbose:
            print(f"{tour}: initial length={big.tour_length(tour):.2f}")
            print(f"{final_tour}: final length={final_length:.2f}")
        lengths.append(final_length)
        if best_tour is None or final_length < big.tour_length(best_tour):
            best_tour = final_tour

    # Print statistics
    arr = np.array(lengths)
    print(f"min: {arr.min():.2f}, max: {arr.max():.2f}, mean: {arr.mean():.2f}, "
          f"median: {np.median(arr):.2f}, stdev: {arr.std():.2f}")
    
    # Save plots
    plot_histogram(lengths)
    plot_tour(big, best_tour, "best_hill_climb_tour.png",
                   title=f"Best hill-climb tour: {big.tour_length(best_tour):.2f}")


if __name__ == "__main__":
    main()
