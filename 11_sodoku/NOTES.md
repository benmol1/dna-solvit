# Constraint Satisfaction — Sudoku Notes

**Setup:** fill a 9×9 grid so every row, column and 3×3 box holds the digits 1 to 9 once. Goal: solve the puzzle with constraint propagation plus backtracking search, count the guesses, and compare with naive backtracking that uses no propagation.

## The idea

Same choose, try, recurse, undo loop as [N-Queens](../10_backtracking_N-queens/NOTES.md) and the [date puzzle](../AA_MF_date-puzzle/NOTES.md). What is new is that the rules are used to *remove* impossible choices before guessing, and again after every new value is fixed.

| Term | Meaning here |
|---|---|
| State | `candidates`: a dict `(r, c)` → string of the digits still possible in that cell |
| Peers | the 20 other cells sharing a row, column or box with a cell (8 + 8 + 4) |
| Propagation | when a cell has one candidate, remove that digit from all 20 peers, recursively |
| Contradiction | a cell whose candidate string becomes empty |
| Search | pick a cell, try each of its candidates on a copy of the state, recurse |

## The pieces

- **`build_peers`** builds the 20 peers of each cell once. It is asserted to have 20 per cell.
- **Candidates as strings.** A solved cell is a one-character string, an empty cell starts as `"123456789"`. `replace` removes a digit, `len` counts, and the string is immutable so a shallow `dict.copy()` is a safe snapshot.
- **`eliminate(candidates, cell, digit)`** removes a digit from a cell. It returns `False` on an empty cell, and when the cell drops to one digit it eliminates that digit from every peer, which is where the recursion comes from. If the digit is already gone it returns `True` straight away, which stops cells re-triggering each other forever.
- **`assign(candidates, cell, digit)`** means "eliminate every *other* digit from this cell". It returns `False` at the first contradiction, so the state may be left half-updated. That is why search always assigns on a copy.
- **`propagate`** applies every given once by eliminating its digit from its peers.
- **MRV search** picks the unsolved cell with the fewest candidates (`min` over a dict of unsolved cells), copies the state, assigns each candidate in turn, and returns the first solved grid, or `None`.
- **Naive search** has no candidates at all. State is an 81-character string, the next cell is `grid.find("0")`, and a digit is tried if no peer already holds it. A new string is built for each placement, so there is no undo step.

## What counts as a guess

One guess is one digit tried in `search`, counted *before* checking whether it works. For naive search that is each of the nine digits tried at a cell. For MRV search it is each remaining candidate passed to `assign`. Applying the givens at the start is not a guess.

The two counts are not perfectly comparable. Naive search pays for digits that `is_safe` rejects immediately, while MRV search has already dropped those from the candidate list. Counting only digits that pass `is_safe` would be a fairer comparison.

## Results

### The assigned puzzle (the one in `problem.md`)

| Method | Guesses | Time |
|---|---|---|
| Propagation only | 0 (solves all 81 cells) | ~0.3 ms |
| Propagation, then MRV search | 0 | ~0.4 ms |
| Naive search | 1,605 | ~1.6 ms |
| MRV search without initial propagation | 2,506 | ~15 ms |

Propagation alone solves it, so propagate+MRV needs no guesses and the ratio naive / propagate+MRV is 1,605 / 0, which is undefined. The top row is `4 8 3 9 2 1 6 5 7`, as the problem states.

### AI Escargot (a hard puzzle)

| Method | Guesses | Time |
|---|---|---|
| Propagation only | 0 (stalls at 24 of 81 cells) | ~0.35 ms |
| Propagation, then MRV search | 22 | ~1.3 ms |
| Naive search | 8,892 | ~137 ms |
| MRV search without initial propagation | 32,693 | ~367 ms |

Here the ratio is defined: **8,892 / 22 ≈ 404**, about 2.6 orders of magnitude. Propagation removes 297 of the 537 candidates (537 = 24 givens + 57 empty cells × 9; 240 remain) but fixes no new cells, so search is needed.

## Notes

- **Propagation vs search.** On the easy puzzle, propagation alone is enough. On AI Escargot it stalls and MRV search finishes the job in 22 guesses.
- **MRV needs propagation to work.** Run on the raw grid, MRV made more guesses than naive search (2,506 vs 1,605 and 32,693 vs 8,892). Every empty cell still lists all nine digits, so "fewest remaining values" mostly measures noise, and ties go to the first cell in dict order. After a guess MRV drifts to the cells that guess just shrank, not to the most constrained part of the real board. This is a hypothesis from reading the behaviour, not something instrumented. Propagating first fixes it, which is why that is the run used for the ratio.
- **Why copy the state.** `assign` can fail halfway, leaving the dict partly changed. Search assigns on `candidates.copy()` so a failed digit leaves the original intact. N-Queens undid each move by hand, but one assignment can change dozens of cells, so copying is simpler.
- **A single run is noisy at this scale.** The easy puzzle runs in microseconds, so timings and any time ratio vary from run to run. Guess counts are deterministic.

## Extension (not done)

- Full AC-3 arc consistency.
- Puzzle generation: remove digits from a solved grid while the solution stays unique, to see how few clues can be reached (the proven minimum is 17).
