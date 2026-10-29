# How the recursive search works (naive search as the example)

This walks through `solve_naive_search` in [search.py](search.py) step by step. The MRV search has the same shape, and the differences are at the end.

## The code

```python
def search(grid):
    next_empty_cell = grid.find("0")
    if next_empty_cell == -1:                  # (1) nothing left to fill
        return grid

    for digit in "123456789":                  # (2) try each choice for this cell
        if not is_safe(grid, next_empty_cell, digit):
            continue                           #     skip digits that break a rule

        guess_count += 1
        new_grid = grid[:next_empty_cell] + digit + grid[next_empty_cell + 1 :]

        result = search(new_grid)              # (3) commit to the digit, go deeper
        if result:                             # (4) deeper call found a solution
            return result                      #     pass it straight back up

    return None                                # (5) no digit worked: dead end
```

## The one idea to hold on to

**Each call to `search` is responsible for exactly one cell, the first empty one.** It does not solve the whole puzzle. It answers one question:

> "Given this grid, can the cell I'm looking at be filled with some digit so that the *rest* of the puzzle can be finished?"

It doesn't work out the rest itself. It places a digit and hands the new grid to another copy of itself, trusting that copy to answer the same question for the next cell.

A call can only end in one of two ways:

| Outcome | When | What it returns |
|---|---|---|
| Success | no `"0"` left in the grid (line 1) | the finished grid |
| Failure | every digit was skipped or led to a failed deeper call (line 5) | `None` |

Everything else is plumbing for passing those two results back up the chain.

## The part that is easy to stumble on

The line `result = search(new_grid)` is where the function pauses. The `for` loop is **paused in the middle**, not abandoned. When the deeper call returns, one of two things happens:

- It returns a grid, which is truthy. Line 4 returns it immediately and the whole chain unwinds with the answer.
- It returns `None`, which is falsy. Line 4 does nothing, the loop moves on to the **next digit**, and this call tries again.

So `None` means "that choice was a dead end". The loop carrying on is the backtracking. There is no explicit undo step.

## Why there is no undo

`grid` is a string, and strings can't be changed in place. `new_grid = ...` builds a **new** string and leaves `grid` untouched. So when a deeper call fails and we return to this level, `grid` is still exactly what it was before we tried the digit. Nothing needs restoring.

(This is also why the MRV search copies the candidates dict before each `assign`. A dict can be changed in place, so the copy plays the role that string immutability plays here.)

## A small worked example

Suppose a grid has three empty cells, `A`, `B`, `C`, in reading order. To keep it short, imagine that the rules allow these digits:

- `A`: 1 or 2
- `B`: depends on what `A` is. After `A=1` it can be 2 or 3. After `A=2` it can be 1.
- `C`: after `A=1, B=2` there is nothing allowed. After `A=1, B=3` only 2 is allowed.

The calls form a tree. Each box is one call to `search`, and each arrow is one digit that passed `is_safe`:

```
                        search(A,B,C empty)
                         looks at A
                        /                \
                  try 1                   try 2   (never reached)
                    |
              search(A=1)
               looks at B
              /          \
        try 2             try 3
          |                 |
    search(A=1,B=2)    search(A=1,B=3)
     looks at C         looks at C
     no digit safe          |
          |               try 2
      return None           |
          X             search(A=1,B=3,C=2)
                         no "0" left
                              |
                        return the grid  <-- solution
```

Reading it in the order the computer runs it:

1. The top call looks at `A`. Digit 1 is safe, so it builds a new grid and calls `search`. The top call's loop is now paused.
2. That call looks at `B`. Digit 2 is safe, so it calls `search` again.
3. That call looks at `C` and finds no safe digit. The loop finishes without placing anything, so it hits line 5 and returns `None`.
4. Back in the `B` call, `result` is `None`, so the loop continues. Digit 3 is safe, so it calls `search` again.
5. The `C` call places 2. No `"0"` is left, so the next call hits line 1 and returns the full grid.
6. The grid is returned up through each paused call, because each one sees a truthy `result` and returns it. The `A=2` branch is never explored.

## The call stack at the moment of the first dead end

Each paused call is a frame on the stack, and each remembers where it was in its `for` loop. This is the picture at step 3 above:

```
 top of stack  ->  search(A=1, B=2)   looking at C, no digit works, about to return None
                   search(A=1)        looking at B, paused on digit 2
                   search(empty)      looking at A, paused on digit 1
```

When the top frame returns `None`, it is removed. The `B` frame wakes up exactly where it paused, which is just after `result = search(new_grid)`, and moves on to digit 3. That is all backtracking is: **popping a frame and resuming the loop in the frame below.**

## How `guess_count` works

`guess_count` is defined in the outer function and changed inside `search`, hence `nonlocal`. Every call shares the same counter. It goes up each time a digit passes `is_safe` and is placed, whether or not that placement later turns out to be a dead end.

## How the MRV search differs

`solve_mrv_search` has the same shape: a base case, a loop over choices, a recursive call, `if result: return result`, and `return None` at the end. It differs in three ways:

| | Naive search | MRV search |
|---|---|---|
| State | an 81-character string | a dict of candidates per cell |
| Which cell next | the first `"0"` | the unsolved cell with the fewest candidates |
| Which digits to try | all nine, skipping unsafe ones | only that cell's remaining candidates |
| After placing a digit | nothing else happens | `assign` also removes the digit from all peers, which can fix other cells and so on |
| "Undo" | a new string each time | a `candidates.copy()` before each `assign` |
| Base case | no `"0"` left | every cell has exactly one candidate |
| Failure signal | no safe digit, loop ends | `assign` returns `False` (a cell ran out of candidates), or the loop ends |

Because propagation shrinks the options after every guess, the MRV search's tree is much smaller. That is why it needed 22 guesses where the naive search needed 8,892 in the propagation-then-MRV run.

## Things to try

- Add `print("  " * depth, "placing", digit, "at", next_empty_cell)` inside `search`, with a `depth` argument that goes up by one on each recursive call. The indented output is the tree above, drawn by your own puzzle.
- Run it on `puzzle_easy` first. The tree is small enough to read.
