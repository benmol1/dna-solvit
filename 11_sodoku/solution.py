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


def search(candidates):
    if all(len(v) == 1 for v in candidates.values()): return candidates

    unsolved = {k:v for k,v in candidates.items() if len(v) > 1}
    cell = min(unsolved, key=lambda c: len(unsolved[c]))

    for digit in candidates[cell]:
        candidates_copy = candidates.copy()
        if assign(candidates_copy, cell, digit):
            result = search(candidates_copy)
            if result: return result

    return None


peers = build_peers()

def propagation_only(candidates):
    start = time.perf_counter()

    # eliminate all the possibilities that are ruled out by the starting problem
    for cell, cands in candidates.items():
        if len(cands) == 1:
            for peer in peers[cell]:
                if not eliminate(candidates, peer, cands):
                    raise ValueError(f"Contradiction at {peer}")

    elapsed = time.perf_counter() - start

    print(f"\nPropogate and eliminate candidates. Assigned values: {count_assigned_cells(candidates)}")
    print(f"Time elapsed: {format_elapsed_time(elapsed)}")
    print_puzzle(to_string(candidates))

    return elapsed


def search_only(candidates):
    start = time.perf_counter()
    solution = search(candidates)
    elapsed = time.perf_counter() - start

    print(f"\nSearch result. Assigned values: {count_assigned_cells(solution)}")
    print(f"Time elapsed: {format_elapsed_time(elapsed)}")
    print_puzzle(to_string(solution))

    return elapsed


def main():
    
    candidates = parse(puzzle)

    print("Input puzzle:")
    print_puzzle(puzzle)

    print(f"Puzzle parsed. Assigned values: {count_assigned_cells(candidates)}")
    print(f"Assigned values in puzzle: {len(puzzle.replace("0", ""))}")

    search_time = search_only(candidates)

    propagation_time = propagation_only(candidates)

    print(f"\nSearch / propagation time ratio: {search_time / propagation_time:.2f}")



if __name__ == "__main__":
    main()