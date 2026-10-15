# Heuristic Search: 8-Puzzle — Notes

**Setup:** 8-puzzle with start = `(7,2,4,5,0,6,8,3,1)` and goal = `(0,1,2,3,4,5,6,7,8)` (0 is the blank). Goal: implement misplaced-tile and Manhattan heuristics, run A* with each, compare nodes expanded, verify dominance empirically, then try an inadmissible heuristic (3 × Manhattan).

## Progress

- [x] Admissibility: what it is and why A* needs it
- [x] Why the blank must be excluded from both heuristics
- [x] `md` (Manhattan) and `misplaced_tiles` implemented in `solution.py`
- [x] Dominance argument (MD ≥ MP) and empirical check over 1,000 random solvable states
- [x] A* with each heuristic: both find 26 moves, nodes expanded recorded vs BFS (~173,800)
- [x] Sabotage experiment: 3 × Manhattan returns 30 moves on the given start state
- [ ] Extension (skipped): IDA*, linear conflict

## Results

| Search | Moves | Expanded | vs BFS (~173,800) |
|---|---|---|---|
| BFS | 26 | ~173,800 | 1× |
| A*, misplaced tiles | 26 | 31,635 | ~5.5× fewer |
| A*, Manhattan | 26 | 1,492 | ~116× fewer |
| A*, 3 × Manhattan (inadmissible) | **30** | 460 | ~378× fewer |

- The reference figures (≈33,100 and ≈2,000) are approximate. The exact counts depend on heap tie-breaking (here `(f, h, state)`) and on how "expanded" is defined (popped, not discovered).
- Both admissible heuristics are optimal; Manhattan does about 21× less work than misplaced tiles. That is dominance paying off.

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

- The inequality is not strict: a tie happens exactly when every misplaced tile is one square from home (e.g. the one-move state above, or three tiles rotated around a 2×2 block).
- Strict example: `(1,2,3,0,4,5,6,7,8)` has MP = 3, MD = 5 (tile 3 contributes distance 3).
- One state with MD < MP would disprove dominance.

**Empirical check (1,000 random solvable states, 100-step random walks from the goal):** `dominant_count` = 1000 (MD ≥ MP every time), `equal_count` = 14. So MD is strictly larger in 98.6% of states. The ties are most likely walks that ended close to the goal.

## Sabotage: 3 × Manhattan

- On the given start state it expanded **fewer** nodes (460 vs 1,492) but returned **30** moves, not 26. Prediction "more nodes" was wrong; "maybe still optimal" turned out to be "no".
- Tripling `h` outweighs the cost paid so far (`g`) in `f = g + h`, so the search turns greedy: fast, but nothing guarantees the first goal popped is the cheapest.
- One state returning the optimal length would not have shown it is safe. Overestimating only *can* produce a worse path.
- **Why 30 and not 27–29:** the blank alternates square colour (chessboard) on every move, so every solution has the same parity. The blank starts at index 4 (centre) and ends at index 0 (corner), both with `row + col` of the matching parity, so solution lengths are all even: 26, 28, 30... The full solvability rule (permutation/inversion parity) was deliberately left for later.

## Implementation notes (`solution.py`)

- `md(state, include_blank=False)`: sums `|row - goal_row| + |col - goal_col|` per tile, with `row = i // 3`, `col = i % 3`.
- `misplaced_tiles(state, include_blank=False)`: loop over `zip(state, goal)`, count positions that differ, skipping the blank unless `include_blank`. (A more compact `sum(...)` version was tried and reverted as too aggressive; the explicit loop stays.)
- `get_neighbours(state)`: copied from the 7_search work; only adds moves that stay on the board (2 neighbours in a corner, 3 on an edge, 4 in the centre).
- `random_solvable_state(num_moves=100)`: random walk from the goal using `get_neighbours`. Moves are reversible, so every state reached is solvable. A random walk can undo its own moves, so the state is usually closer than `num_moves` from the goal (fine here, but not for a known difficulty). `random.shuffle` is no good: half of all 9! orderings are unsolvable.
- `assert_md_dominates_mp()`: counts states with `md >= mp` and with `md == mp` over 1,000 random solvable states.
- `astar_search(h_function=md)`: adapted from the 8_search2 A*. Heap entries `(f, h, state)`, `g` dict as the visited record, `parents` for path reconstruction, `expanded` set to skip stale heap entries. `get_path_from_parents` walks back from the goal.

## Gotchas

- **`from numpy import random` clobbers the stdlib.** `numpy.random.choice` turns a list of equal-length tuples into a 2D array (`ValueError: a must be 1-dimensional`) and would return an `ndarray`, not a tuple. Use `import random` (stdlib), or `neighbours[np.random.randint(len(neighbours))]`.
- **Pass `goal` consistently.** `md` and `misplaced_tiles` read the global `goal`; `random_solvable_state` now does too instead of taking it as a parameter.
- **Bare `assert` is silent on success and anonymous on failure**, so print a message and include the offending state in the assert message.
- **Expand `current`, not the global `state`.** `get_neighbours(state)` inside A* kept expanding the start's neighbours, so the goal was never reached and `get_path_from_parents` failed (probably a `KeyError`) at the call site, far from the real bug.
- **Don't pass `goal` into `md`.** `h_function(neighbour, goal)` silently bound `goal` to `include_blank`, turning on the inadmissible version. It doesn't crash; it just gives the wrong heuristic.

## Open questions / not done

- Extension: IDA* (linear memory) and linear conflict (+2 per reversed pair in goal row/column; check it stays admissible). Skipped.
- Permutation (inversion) parity, the full solvability rule. Skipped for now.
- Weighted A* (`w × h`) is the principled version of the sabotage experiment: with `w = 3`, the cost is at most 3× optimal. Not explored here.
