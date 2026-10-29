from dna_solvit.utils import format_elapsed_time


def build_peers():
    """Return {(r, c): set of the 20 peer cells} for a 9x9 grid."""
    peers = {}
    for r in range(9):
        for c in range(9):
            # get the row and column peers
            row_peers = [(r, i) for i in range(9) if i != c]
            col_peers = [(i, c) for i in range(9) if i != r]

            # get the coordinates of the top-left corner of the box containing (r,c)
            br, bc = 3 * (r // 3), 3 * (c // 3)

            # get the box peers
            box_peers = [
                (br + dr, bc + dc)
                for dr in range(3)
                for dc in range(3)
                if (br + dr, bc + dc) != (r, c)
            ]

            peers[(r, c)] = set(row_peers + col_peers + box_peers)

    assert all(len(p) == 20 for p in peers.values())
    return peers


peers = build_peers()


def parse(input_puzzle):
    """Convert an 81-character puzzle string into a candidates dict.

    Empty cells ("0") get all nine candidates; given digits get just themselves.
    """
    candidates = {}
    for i, ch in enumerate(input_puzzle):
        r, c = divmod(i, 9)
        if ch == "0":
            candidates[(r, c)] = "123456789"
        else:
            candidates[(r, c)] = ch
    return candidates


def count_assigned_cells(candidates):
    """Return the number of cells that have exactly one candidate left."""
    return sum(len(cands) == 1 for cands in candidates.values())


def total_candidates(candidates):
    """Return the total number of candidate digits remaining across all cells."""
    return sum(len(cands) for cands in candidates.values())


def to_string(candidates):
    """Return an 81-character grid string, using "0" for unresolved cells."""
    return "".join(
        candidates[(r, c)] if len(candidates[(r, c)]) == 1 else "0"
        for r in range(9)
        for c in range(9)
    )


def print_puzzle(puzzle):
    """Print an 81-character grid string as nine rows of nine digits."""
    grid = "\n".join(puzzle[i : i + 9] for i in range(0, 81, 9))
    print(grid)


def report(title, solution, elapsed, guess_count, verbose=False):
    """Print the outcome of a solver run: stats and the resulting grid, or a no-solution message."""
    print(f"\n{title}")
    if solution is None:
        print("No solution found")
        return
    # solution is either a grid string (naive solver) or a candidates dict
    grid = solution if isinstance(solution, str) else to_string(solution)
    print(f"Assigned values: {81 - grid.count('0')}")
    print(f"Time elapsed: {format_elapsed_time(elapsed)}")
    print(f"Guess count: {guess_count:,}")
    if verbose:
        print_puzzle(grid)
