# Backtracking — N-Queens Notes

**Setup:** place N queens on an N×N board so that no two share a row, column or diagonal. Goal: count every solution for N = 6 and N = 8, count the nodes the search visits, and compare that with brute force.

## The idea

The same choose, try, recurse, undo loop as the [date puzzle](../AA_MF_date-puzzle/NOTES.md), but with a much simpler state.

| Term | Meaning here |
|---|---|
| State | which columns and diagonals are taken, and the column of each queen placed so far |
| Successor | one queen in the next row, in a column that is still safe |
| Goal | `r == N`: every row has a queen |
| Pruning | skip any square that shares a column or diagonal with a queen already placed |

**One queen per row.** Two queens can never share a row in a solution, so instead of choosing squares from the whole board, `search(r)` fills row `r` and the only choice is the column. This is the pruning that matters most: it removes every arrangement with two queens in a row before they are ever generated.

## The O(1) safety check

Three sets hold what is already taken. With row 0 at the top:

| Set | Label for square `(r, c)` | Identifies |
|---|---|---|
| `occupied_cols` | `c` | a column |
| `occupied_diag1` | `r + c` | a ↗ diagonal (constant as `r` goes down and `c` goes up) |
| `occupied_diag2` | `r - c` | a ↘ diagonal (constant as `r` and `c` both increase) |

A square is safe if none of its three labels is in its set. A set lookup is O(1), so the check does not grow with the number of queens, unlike comparing the new queen against every placed queen.

`place_queen` adds the three labels and `remove_queen` removes them, so the undo step restores the sets exactly. The `queens` list records the column of each row, and `solutions.append(queens[:])` copies it at the base case. Without the `[:]`, every stored solution would be the same list, empty by the end.

## Results

| N | Solutions | Placements | Brute force C(N², N) | Pruning ratio |
|---|---|---|---|---|
| 4 | 2 | 16 | 1,820 | 1.1e2 |
| 6 | 4 | 152 | 1,947,792 | 1.3e4 |
| 8 | 92 | 2,056 | 4,426,165,368 | 2.2e6 |
| 12 | 14,200 | 856,188 | 1.0e17 | 1.2e11 |

`placements` counts every queen placed, so it is the number of nodes visited in the search tree, not counting the root. The pruning ratio is the brute-force count divided by that. It grows quickly with N because brute force grows like C(N², N) while the pruned tree grows far more slowly.

The first N = 8 solution found is `[0, 4, 7, 5, 2, 6, 1, 3]` (the column of the queen in each row), found after 113 placements when the search stops at the first solution.

## Notes

- **`find_all`:** with `find_all=True`, `search` never returns `True`, so it backtracks out of every branch, including the ones that found a solution, and so counts all of them. This is the same early-exit signal as in the date puzzle.
- **Symmetry:** the 92 solutions for N = 8 are 12 fundamental ones plus their rotations and reflections. Only searching the first-row columns `0..N/2` and doubling the count would use the left-right mirror and roughly halve the work.
- **Same family:** Sudoku, the date puzzle and constraint satisfaction in general use this pattern. The better the pruning, the smaller the tree.
