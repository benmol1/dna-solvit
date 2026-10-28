import time

from dna_solvit.utils import format_elapsed_time

puzzle =("003020600900305001001806400"
        "008102900700000008006708200"
        "002609500800203009005010300")



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
           
            peers[(r,c)] = set(row_peers + col_peers + box_peers)
    
    assert all(len(p) == 20 for p in peers.values())
    return peers


def parse(input_puzzle):
    candidates = {}
    for i, ch in enumerate(input_puzzle):
        r, c = divmod(i, 9)
        if ch == "0":
            candidates[(r,c)] = "123456789"
        else:
            candidates[(r,c)] = ch
    return candidates


def count_assigned_cells(candidates):
    return sum(len(cands) == 1 for cands in candidates.values())

def to_string(candidates):
    return "".join(
        candidates[(r, c)] if len(candidates[(r, c)]) == 1 else "0"
        for r in range(9)
        for c in range(9)
    )

def print_puzzle(puzzle):
    grid = "\n".join(puzzle[i:i + 9] for i in range(0, 81, 9))
    print(grid)


def assign(candidates, cell, digit):
    # If the digit is not in the candidates for this cell then we should never be attempting to assign it, so return False
    if digit not in candidates[cell]:
        return False   

    # Make a string of all the other candidates (excluding the digit we have chosen to assign)
    others = candidates[cell].replace(digit, "")

    # Eliminate all of the other candidates from this cell (NB: also recursively eliminates from peers where applicable)
    return all(eliminate(candidates, cell, d) for d in others)


def eliminate(candidates, cell, digit):
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


peers = build_peers()

def propagate(candidates):
    for cell, cands in candidates.items():
        if len(cands) == 1:
            for peer in peers[cell]:
                if not eliminate(candidates, peer, cands):
                    raise ValueError(f"Contradiction at {peer}")

def is_safe(grid, cell_index, digit):
    r,c = divmod(cell_index,9)
    return all(grid[pr*9 + pc] != digit for pr, pc in peers[(r,c)])      

def solve_naive_search(grid):
    
    guess_count = 0

    def search(grid):
        nonlocal guess_count
    
        next_empty_cell = grid.find("0")
        if next_empty_cell == -1:
            return grid

        for digit in "123456789":
            if not is_safe(grid, next_empty_cell, digit):
                 continue   
            
            # place digit in grid
            guess_count +=1
            new_grid = grid[:next_empty_cell] + digit + grid[next_empty_cell + 1:]

            result = search(new_grid)
            if result: return result

        return None
    
    solution = search(grid)

    return solution, guess_count


def solve_naive_search_only(grid):
    start = time.perf_counter()
    solution, guess_count = solve_naive_search(grid)
    elapsed = time.perf_counter() - start

    report("Naive search only", solution, elapsed, guess_count)

    return elapsed, guess_count


def solve_propagation_only(candidates):
    start = time.perf_counter()

    # eliminate all the possibilities that are ruled out by the starting problem
    propagate(candidates)

    elapsed = time.perf_counter() - start

    report("Propagation only", solution=candidates, elapsed=elapsed, guess_count=0)

    return elapsed


def solve_prop_then_mrv_search(candidates):
    start = time.perf_counter()
    propagate(candidates)
    solution, guess_count = solve_mrv_search(candidates)
    elapsed = time.perf_counter() - start

    report("Propagation then MRV search", solution, elapsed, guess_count)

    return elapsed, guess_count


def report(title, solution, elapsed, guess_count):
    print(f"\n{title}")
    if solution is None:
        print("No solution found")
        return
    # solution is either a grid string (naive solver) or a candidates dict
    grid = solution if isinstance(solution, str) else to_string(solution)
    print(f"Assigned values: {81 - grid.count('0')}")
    print(f"Time elapsed: {format_elapsed_time(elapsed)}")
    print(f"Guess count: {guess_count}")
    print_puzzle(grid)


def solve_mrv_search(candidates):
    guess_count = 0

    def search(candidates):
        nonlocal guess_count
        if all(len(v) == 1 for v in candidates.values()): return candidates

        unsolved = {k:v for k,v in candidates.items() if len(v) > 1}
        cell = min(unsolved, key=lambda c: len(unsolved[c]))

        for digit in candidates[cell]:
            candidates_copy = candidates.copy()
            guess_count += 1
            if assign(candidates_copy, cell, digit):
                result = search(candidates_copy)
                if result: return result

        return None

    solution = search(candidates)

    return solution, guess_count


def solve_mrv_search_only(candidates):
    start = time.perf_counter()
    solution, guess_count = solve_mrv_search(candidates)
    elapsed = time.perf_counter() - start

    report("MRV search only", solution, elapsed, guess_count)

    return elapsed, guess_count


def main():
    
    candidates_input = parse(puzzle)
    candidates_search = candidates_input.copy()
    candidates_propagation = candidates_input.copy()
    candidates_mix = candidates_input.copy()

    print("Input puzzle:")
    print_puzzle(puzzle)

    print(f"Puzzle parsed. Assigned values: {count_assigned_cells(candidates_input)}")
    print(f"Assigned values in puzzle: {len(puzzle.replace("0", ""))}")

    search_time, _ = solve_mrv_search_only(candidates_search)
    propagation_time = solve_propagation_only(candidates_propagation)
    mix_time, _ = solve_prop_then_mrv_search(candidates_mix)
    naive_search_time, _ = solve_naive_search_only(puzzle)

    


if __name__ == "__main__":
    main()