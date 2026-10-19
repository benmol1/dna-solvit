import time
from math import comb

from rich.console import Console
from rich.text import Text

from dna_solvit.utils import format_elapsed_time


def solve(N, find_all=False):

    queens = [None] * N
    solutions = []
    placements = 0
    occupied_cols, occupied_diag1, occupied_diag2 = set(), set(), set()

    def safe(r, c):
        if (
            (c in occupied_cols)
            or (r + c in occupied_diag1)
            or (r - c in occupied_diag2)
        ):
            return False
        return True

    def place_queen(r, c):
        occupied_cols.add(c)
        occupied_diag1.add(r + c)
        occupied_diag2.add(r - c)
        queens[r] = c

    def remove_queen(r, c):
        occupied_cols.remove(c)
        occupied_diag1.remove(r + c)
        occupied_diag2.remove(r - c)
        queens[r] = None

    def search(r):
        nonlocal placements
        if r == N:
            solutions.append(queens[:])
            return not find_all
        for c in range(N):
            if not safe(r, c):
                continue
            place_queen(r, c)
            placements += 1
            if search(r + 1):
                return True
            remove_queen(r, c)
        return False

    search(0)
    return solutions, placements


def render(N, solution):
    text = Text()
    for r in range(N):
        for c in range(N):
            light = (r + c) % 2 == 0
            bg = "white" if light else "grey11"
            if solution[r] == c:
                piece, fg = "Q", "red"
            else:
                piece, fg = " ", "black"
            text.append(f" {piece} ", style=f"bold {fg} on {bg}")
        text.append("\n")
    return text


def main():
    N = 12
    start = time.perf_counter()
    solutions, placements = solve(N, find_all=True)
    elapsed = time.perf_counter() - start

    pruning_ratio = comb(N * N, N) / placements

    print(
        f"{N}x{N} grid\n# solutions:\t{len(solutions):,}\n"
        f"# placements:\t{placements:,}\n"
        f"pruning ratio:\t{pruning_ratio:.1e}\n"
        f"time elapsed:\t{format_elapsed_time(elapsed)}\n"
    )

    print("Solution[0]:")
    Console().print(render(N, solutions[0]))


if __name__ == "__main__":
    main()
