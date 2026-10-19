# Backtracking Search — A-Puzzle-A-Day Notes

**Setup:** the DragonFjord "A-Puzzle-A-Day" board has 43 squares: 12 months and 31 days. Eight pieces cover 41 squares, so for any date, placing them all leaves exactly two squares showing: that month and that day. Pieces may be rotated and flipped. Goal: given a date, find a placement of all eight pieces.

## The idea

This is an **exact cover** problem: every square except the two date squares must be covered by exactly one piece. The standard tool is **depth-first backtracking** (also called backtracking search, or exhaustive search with pruning).

| Term | Meaning here |
|---|---|
| State | the grid so far, plus which pieces are still unused |
| Successor | one more piece, in one orientation, placed on the grid |
| Goal | no empty squares left |
| Path cost | none, only the final arrangement matters |

There is no "move" and no path cost, so A* has nothing to optimise: no placement is cheaper than another, and we only want any state that satisfies the constraints. Depth-first search fits because every solution is exactly 8 placements deep.

## How the search works

```
search():
    target = first empty square (reading order)
    if none: solution found
    for each unused piece, for each orientation:
        if it covers target and fits:
            place it
            if search(): stop            # only when find_all is False
            undo the placement           # <- the "backtrack"
    return False                         # dead end
```

1. **Choose** the next square to fill.
2. **Try** each piece and orientation that fits.
3. **Recurse** with that piece placed.
4. **Undo** the placement if the recursion fails, then try the next option.

The undo step is what makes it backtracking: the grid is one shared object that gets modified and restored, not copied at each step. A branch that cannot be completed returns `False`, and each caller undoes its piece and tries its next option, so the search climbs back up only as far as it needs to.

## Why the "first empty square" rule works

Every solution must cover the first empty square (in reading order) with *some* piece. So instead of asking where each piece could go, we ask which piece covers this square, and that is a much smaller question.

For a given orientation, the target square must be covered by the piece's **own first cell** (its top-left in reading order). Any other cell of the piece would put the piece's first cell earlier in reading order, and every earlier square is already filled. So each orientation has exactly one candidate position, not one per cell.

This also removes duplicates: a given arrangement is generated in only one order (smallest square first), not in every order of placing the same pieces. Without it, the search would revisit the same partial boards many times over, once per ordering.

## Pruning

The search is cheap because it prunes. `fits` rejects a placement as soon as it overlaps a filled square or runs off the board, and the whole subtree below it is never visited. The bounds check matters in Python: a negative index would wrap around to the far side of the grid instead of raising an error.

## Results

| Date | Mode | Solutions | Placements tried |
|---|---|---|---|
| 17 Oct | first solution only | 1 | 1,351 |
| 17 Oct | `--all` | 48 | 33,407 |

`--all` runs `find_all=True`: the search never stops early, so it explores the whole pruned tree and counts every solution. Rotated or mirrored boards are not merged, since the date squares fix the board's orientation.

## Where it goes next

- **Better pruning:** flood-fill the empty regions after each placement and backtrack if any region has fewer than 5 squares, since no piece could fill it.
- **Algorithm X / Dancing Links:** Knuth's algorithm for exact cover. It is the same search, but it picks the *most constrained* square instead of the first, and uses linked lists so that undoing a choice is cheap.
- **Same family:** Sudoku, N-queens, scheduling and constraint satisfaction all use this choose, try, recurse, undo pattern.
