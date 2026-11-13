import random
import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent

cities = [(77,44),(86,70),(9,98),(76,79),(13,45),(37,93),
          (64,82),(44,23),(55,6),(83,63),(76,35),(97,89)]

def two_opt(tour, i, j):
    """Return a new tour with positions i..j (inclusive) reversed."""
    return tour[:i] + tour[i:j+1][::-1] + tour[j+1:]


def city_distance(city_a, city_b):
    (x1, y1), (x2, y2) = city_a, city_b
    return math.hypot(x2 - x1, y2 - y1)



def tour_length(tour):
    total_length = 0
    for ii, _ in enumerate(tour):
        total_length += city_distance(cities[tour[ii-1]], cities[tour[ii]])

    return total_length


def plot_tour(tour, title=None, ax=None):
    """Draw a closed tour over the cities, numbering each stop."""
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))

    xs = [cities[i][0] for i in tour] + [cities[tour[0]][0]]
    ys = [cities[i][1] for i in tour] + [cities[tour[0]][1]]

    ax.plot(xs, ys, "-o", color="tab:blue", markersize=6)
    for step, city in enumerate(tour):
        ax.annotate(step, cities[city], textcoords="offset points", xytext=(5, 5))
    ax.plot(*cities[tour[0]], "o", color="tab:red", markersize=10)  # start city

    ax.set_title(title or f"Tour length = {tour_length(tour):.2f}")
    ax.set_aspect("equal")
    return ax


def main():

    test_tour = [5, 7, 6, 9, 2, 0, 3, 11, 8, 4, 1, 10]
    # random_tour = random.sample(range(12), 12)

    tour = two_opt(test_tour,1,3)
    tour = two_opt(tour,1,2)
    tour = two_opt(tour,3,4)
    tour = two_opt(tour,2,5)
    tour = two_opt(tour,3,9)

    print(f"{tour}: length={tour_length(tour):.2f}")

    plot_tour(tour)
    plt.savefig(OUT_DIR / "random_tour.png", dpi=150, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()