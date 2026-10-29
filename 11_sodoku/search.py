from pathlib import Path

from sudoku_utils import peers

NAIVE_TREE_PATH = Path(__file__).parent / "naive_tree.txt"


def assign(candidates, cell, digit):
    """Assign digit to cell by eliminating all other candidates from it.

    Mutates candidates (eliminations propagate to peers). Returns False if the
    digit is not a candidate or a contradiction arises, otherwise True.
    """
    # If the digit is not in the candidates for this cell then we should never be attempting to assign it, so return False
    if digit not in candidates[cell]:
        return False

    # Make a string of all the other candidates (excluding the digit we have chosen to assign)
    others = candidates[cell].replace(digit, "")

    # Eliminate all of the other candidates from this cell (NB: also recursively eliminates from peers where applicable)
    return all(eliminate(candidates, cell, d) for d in others)


def eliminate(candidates, cell, digit):
    """Remove digit from the candidates of cell, propagating to peers.

    If cell is reduced to a single candidate, that digit is eliminated from all
    its peers recursively. Mutates candidates. Returns False on contradiction
    (a cell left with no candidates), otherwise True.
    """
    # If this digit is not in the candidates list for the cell, then no action required. Return True
    if digit not in candidates[cell]:
        return True

    # Remove the digit from this cell's list of candidates
    candidates[cell] = candidates[cell].replace(digit, "")

    # Check that the string of candidates for this cell is not empty - it never should be for a valid solution.
    if not candidates[cell]:
        return False

    # If we now only have one candidate for this cell, eliminate that digit from all of the peers
    if len(candidates[cell]) == 1:
        for peer in peers[cell]:
            if not eliminate(candidates, peer, candidates[cell]):
                return False
    return True


def propagate(candidates):
    """Eliminate the value of every already-solved cell from its peers.

    Mutates candidates. Raises ValueError if a contradiction is found.
    """
    for cell, cands in candidates.items():
        if len(cands) != 1:
            continue
        for peer in peers[cell]:
            if not eliminate(candidates, peer, cands):
                raise ValueError(f"Contradiction at {peer}")


def is_safe(grid, cell_index, digit):
    """Return True if no peer of the cell at cell_index already holds digit."""
    r, c = divmod(cell_index, 9)
    return all(grid[pr * 9 + pc] != digit for pr, pc in peers[(r, c)])


def solve_naive_search(grid, verbose=False):
    """Solve a grid string by plain backtracking over the first empty cell.

    If verbose, the search tree is written to naive_tree.txt next to this file.
    Returns (solution, guess_count); solution is None if there is none.
    """
    guess_count = 0
    tree_file = open(NAIVE_TREE_PATH, "w") if verbose else None

    def search(grid, depth):
        """Fill the first empty cell with each safe digit, recursing; return the solved grid or None."""
        nonlocal guess_count

        next_empty_cell = grid.find("0")
        if next_empty_cell == -1:
            return grid

        for digit in "123456789":
            if not is_safe(grid, next_empty_cell, digit):
                continue

            if tree_file:
                # record the current node of the search tree
                print(
                    f"{depth:02d}: {'  ' * depth}placing {digit} at location {next_empty_cell}",
                    file=tree_file,
                )

            # place digit in grid
            guess_count += 1
            new_grid = grid[:next_empty_cell] + digit + grid[next_empty_cell + 1 :]

            result = search(new_grid, depth+1)
            if result:
                return result

        return None

    try:
        solution = search(grid, 0)
    finally:
        if tree_file:
            tree_file.close()

    return solution, guess_count


def solve_mrv_search(candidates):
    """Solve a candidates dict by backtracking, always branching on the cell with fewest candidates (MRV).

    Returns (solution, guess_count); solution is None if there is none.
    """
    guess_count = 0

    def search(candidates):
        """Branch on the unsolved cell with fewest candidates; return a solved candidates dict or None."""
        nonlocal guess_count
        if all(len(v) == 1 for v in candidates.values()):
            return candidates

        unsolved = {k: v for k, v in candidates.items() if len(v) > 1}
        cell = min(unsolved, key=lambda c: len(unsolved[c]))

        for digit in candidates[cell]:
            candidates_copy = candidates.copy()
            guess_count += 1
            if assign(candidates_copy, cell, digit):
                result = search(candidates_copy)
                if result:
                    return result

        return None

    solution = search(candidates)

    return solution, guess_count
