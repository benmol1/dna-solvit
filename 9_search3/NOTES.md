# Heuristic Search: 8-Puzzle — Notes

**Setup:** 8-puzzle with start = `(7,2,4,5,0,6,8,3,1)` and goal = `(0,1,2,3,4,5,6,7,8)` (0 is the blank). Goal: implement misplaced-tile and Manhattan heuristics, run A* with each, compare nodes expanded, verify dominance empirically, then try an inadmissible heuristic (3 × Manhattan).

## Progress so far

- [x] Admissibility: what it is and why A* needs it
- [x] Why the blank must be excluded from both heuristics
- [x] `md` (Manhattan) and `misplaced_tiles` implemented in `solution.py`
- [x] Dominance argument (MD ≥ MP) and an empirical check over 1,000 random solvable states (written, not yet run at time of writing)
- [ ] A* with each heuristic: confirm 26 moves, record nodes expanded vs BFS (~173,800)
- [ ] Sabotage experiment: 3 × Manhattan
- [ ] Extension: IDA*, linear conflict

## Admissibility

A heuristic is *admissible* if it never overestimates the true remaining cost. A* pops the node with the lowest `f = g + h` and stops when the goal is popped.

- If `h` overstates the cost at a node N on the optimal path, N's `f` is inflated and it can sit behind a worse path in the queue.
- A* would then pop the goal via the worse path and return it with full confidence (not merely "unsure").
- With an admissible `h`, every node still waiting on the optimal path has `f ≤ C*` (the optimal cost), so none can sit behind a goal node costing more. The first goal popped is optimal.

## Why exclude the blank

One move slides exactly one numbered tile by one square; the blank moves the other way. Counting the blank charges for that single move twice.

Test state, one move from the goal: `(1,0,2,3,4,5,6,7,8)`.

| Heuristic | Including blank | Excluding blank | True cost |
|---|---|---|---|
| Manhattan | 2 | 1 | 1 |
| Misplaced | 2 | 1 | 1 |

Including the blank overestimates (2 > 1), so it is inadmissible. Excluding it, a move changes the Manhattan sum by at most 1, so at least `h` moves are needed. For misplaced tiles, a move fixes at most one tile.

## Dominance

Heuristic A *dominates* B if `A(s) ≥ B(s)` for every state `s`. If both are admissible, A* with the dominating one is never worse and usually expands far fewer nodes.

**Argument for MD ≥ MP:** a correctly placed tile adds 0 to both. A misplaced tile adds exactly 1 to MP and at least 1 to MD. Summing over tiles gives MD ≥ MP for every state.

- The inequality is not strict: with every misplaced tile one square from home, MD = MP (the one-move state above).
- Strict example: `(1,2,3,0,4,5,6,7,8)` has MP = 3, MD = 5 (tile 3 contributes distance 3).
- One state with MD < MP would disprove dominance.

## Implementation notes (`solution.py`)

- `md(state, include_blank=False)`: sums `|row - goal_row| + |col - goal_col|` per tile, with `row = i // 3`, `col = i % 3`.
- `misplaced_tiles(state, include_blank=False)`: loop over `zip(state, goal)`, count positions that differ, skipping the blank unless `include_blank`. (A more compact `sum(...)` version was tried and reverted as too aggressive; the explicit loop stays.)
- `get_neighbours(state)`: copied from the 7_search work; only adds moves that stay on the board (2 neighbours in a corner, 3 on an edge, 4 in the centre).
- `random_solvable_state(num_moves=100)`: random walk from the goal using `get_neighbours`. Moves are reversible, so every state reached is solvable. A random walk can undo its own moves, so the state is usually closer than `num_moves` from the goal (fine here, but not for a known difficulty). `random.shuffle` is no good: half of all 9! orderings are unsolvable.
- `assert_md_dominates_mp()`: 1,000 random solvable states, asserts `md >= mp` with the state in the failure message, prints on success.

## Gotchas

- **`from numpy import random` clobbers the stdlib.** `numpy.random.choice` turns a list of equal-length tuples into a 2D array (`ValueError: a must be 1-dimensional`) and would return an `ndarray`, not a tuple. Use `import random` (stdlib), or `neighbours[np.random.randint(len(neighbours))]`.
- **Pass `goal` consistently.** `md` and `misplaced_tiles` read the global `goal`; `random_solvable_state` now does too instead of taking it as a parameter.
- **Bare `assert` is silent on success and anonymous on failure**, so print a message and include the offending state in the assert message.

## Open questions / next steps

- What proportion of the 1,000 random states have MD > MP *strictly*? (No prediction yet. Worth counting.)
- Run A* with both heuristics on the given start state; expect 26 moves, about 33,100 expanded for MP and about 2,000 for MD, against about 173,800 for BFS.
- Sabotage: 3 × Manhattan. Faster? Still optimal? Find a start state where it returns a longer-than-optimal solution.
- Extension: IDA* (linear memory), then linear conflict (+2 per reversed pair in goal row/column) and check it stays admissible.
