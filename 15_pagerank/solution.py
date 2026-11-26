import random
import time

import numpy as np

from dna_solvit.utils import format_elapsed_time


def pagerank_basic(links, d=0.85, verbose=False):
    start = time.perf_counter()
    n = len(links)
    rank = {page: 1 / n for page in links}
    iterations = 0

    while True:
        iterations += 1
        new = {}
        for p in links:
            inflow = 0
            for q in links:
                if p in links[q]:
                    inflow += rank[q] / len(links[q])
            new[p] = (d * inflow) + (1 - d) / n

        change = max(abs(new[p] - rank[p]) for p in links)
        rank = new

        if change < 1e-10:
            break

    elapsed = time.perf_counter() - start
    if verbose:
        print(
            f"### PageRank basic ###\nd={d}. Converged after {iterations} iterations in {format_elapsed_time(elapsed)}."
        )
        for page, score in sorted(rank.items(), key=lambda kv: -kv[1]):
            print(page, f"{score:#.3f}")


def pagerank_matrix(links, d=0.85, method="power", verbose=False):
    """method: 'power' (power iteration), 'inverse' (direct solve), 'eig' (eigenvector)."""
    start = time.perf_counter()
    pages = sorted(links)  # fixed order: A..F
    n = len(pages)

    # Build transition matrix
    idx = {p: i for i, p in enumerate(pages)}
    M = np.zeros((n, n))
    for col, targets in links.items():
        for row in targets:
            M[idx[row], idx[col]] = 1 / len(targets)

    teleport_vector = np.full(n, (1 - d) / n)
    iterations = 0

    if method == "inverse":
        # This is the same Markov chain steady-state maths I used in the factorio quality repo
        Q = np.eye(n) - d * M
        Q_inv = np.linalg.inv(Q)
        rank = Q_inv @ teleport_vector

    elif method == "eig":
        # Fold teleporting into one matrix: every column of G sums to 1
        G = d * M + teleport_vector
        eigvals, eigvecs = np.linalg.eig(G)
        k = np.argmax(eigvals.real)  # eigenvalue 1 is the largest
        v = eigvecs[:, k].real
        rank = v / v.sum()  # normalise (also fixes the sign)
        if verbose:
            print(f"  largest eigenvalue: {eigvals[k].real:.6f}")

    elif method == "power":
        rank = np.full(n, 1 / n)

        # Run iterations
        while True:
            iterations += 1

            rank_new = d * (M @ rank) + teleport_vector
            change = np.max(abs(rank_new - rank))

            if change < 1e-10:
                break
            rank = rank_new

    else:
        raise ValueError(f"unknown method: {method}")
    elapsed = time.perf_counter() - start

    # Print results
    print(f"### PageRank matrix ({method}), d={d}: {format_elapsed_time(elapsed)} ###")
    if verbose:
        if method == "power":
            print(f"Converged after {iterations} iterations")
        for page, score in sorted(zip(pages, rank), key=lambda ps: -ps[1]):
            print(page, f"{score:.3f}")


def get_small_web():
    links = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": ["A"],
        "D": ["A", "C"],
        "E": ["C", "D"],
        "F": ["C", "E"],
    }
    return links


def get_big_web(n):
    pages = [str(i) for i in range(n)]
    links = {p: random.sample(pages, 5) for p in pages}
    return links


def main():
    links = get_big_web(2000)

    # pagerank_basic(links, d=0.85, verbose=False)
    for method in ("power", "inverse", "eig"):
        pagerank_matrix(links, d=0.85, method=method, verbose=False)


if __name__ == "__main__":
    main()
