import time

from search import propagate, solve_mrv_search, solve_naive_search
from sudoku_utils import (
    count_assigned_cells,
    parse,
    print_puzzle,
    report,
    total_candidates,
)

puzzle_easy = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
puzzle_hard = "800000001015400070060008090450020000009604000000010002080700030030000640200060008"
# See https://www.kristanix.com/sudokuepic/worlds-hardest-sudoku.php
puzzle_ai_escargot = "100007090030020008009600500005300900010080002600004000300000010041000007007000300"

def run_naive_search(grid, verbose):
    """Solve with naive backtracking, print a report, and return (elapsed, guess_count)."""
    start = time.perf_counter()
    solution, guess_count = solve_naive_search(grid, verbose)
    elapsed = time.perf_counter() - start

    report("Naive search only", solution, elapsed, guess_count, verbose)

    return elapsed, guess_count


def run_propagation(candidates, verbose):
    """Apply constraint propagation alone, print a report, and return elapsed time."""
    start = time.perf_counter()
    # eliminate all the possibilities that are ruled out by the starting problem
    propagate(candidates)
    elapsed = time.perf_counter() - start

    report("Propagation only", candidates, elapsed, guess_count=0, verbose=verbose)

    return elapsed


def run_prop_then_mrv_search(candidates, verbose):
    """Propagate constraints, then MRV search; print a report and return (elapsed, guess_count)."""
    start = time.perf_counter()
    before = total_candidates(candidates)
    propagate(candidates)
    after = total_candidates(candidates)

    solution, guess_count = solve_mrv_search(candidates)
    elapsed = time.perf_counter() - start

    report("Propagation then MRV search", solution, elapsed, guess_count, verbose)
    print(f"Candidates: {before} -> {after} ({before - after} eliminated)")

    return elapsed, guess_count


def run_mrv_search(candidates, verbose):
    """Solve with MRV search alone, print a report, and return (elapsed, guess_count)."""
    start = time.perf_counter()
    solution, guess_count = solve_mrv_search(candidates)
    elapsed = time.perf_counter() - start

    report("MRV search only", solution, elapsed, guess_count, verbose)

    return elapsed, guess_count


def main():
    """Run each solving strategy on the AI Escargot puzzle and report the results."""
    puzzle = puzzle_ai_escargot
    verbose = False
    
    if verbose:
        print("Input puzzle:")
        print_puzzle(puzzle)

    candidates_input = parse(puzzle)
    print(f"Puzzle parsed. Assigned values: {count_assigned_cells(candidates_input)}")
    print(f"Assigned values in puzzle: {len(puzzle.replace('0', ''))}")

    naive_search_time, naive_guess_count = run_naive_search(puzzle, verbose)
    propagation_time = run_propagation(parse(puzzle), verbose)
    mrv_search_time, mrv_guess_count = run_mrv_search(parse(puzzle), verbose)
    mix_time, mix_guess_count = run_prop_then_mrv_search(parse(puzzle), verbose)

    if mix_guess_count:
        print(f"\nEfficieny ratio of mix vs naive: {naive_guess_count:,} vs {mix_guess_count:,} "
              f"= {naive_guess_count/mix_guess_count:,.0f}x better")
    else:
        print(f"\nMix needed no guesses (naive needed {naive_guess_count:,}), so no ratio")

if __name__ == "__main__":
    main()
