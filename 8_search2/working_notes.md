# Working notes: A* search

## Where I started
- Comfortable with BFS (problem 7) and with Manhattan distance as "horizontal + vertical distance".
- Used `heapq` for uniform-cost search in problem 7, pushing `(running cost, city)`.
- Goal: understand A* and be able to implement it semi-fluently.

## What we covered

**BFS and the frontier**
- The *graph* (the maze, or the road dictionary) is not the *frontier*. The frontier is the collection of discovered-but-not-yet-expanded nodes.
- BFS uses a FIFO queue (`deque`, `popleft`), so nodes are expanded in order of distance from the start. The first time it reaches G, no shorter path exists.
- BFS knows nothing about where G is. On an open grid with 4-direction moves its expanded region is a growing *diamond* (cells exactly n steps away), so it wastes effort in directions away from the goal.

**Manhattan distance is admissible**
- Walls can only make the true path longer, never shorter, so Manhattan distance <= true remaining distance.
- A heuristic that never overestimates is called *admissible*. This is what keeps A* optimal.

**Why not use h alone (greedy best-first)?**
- Ordering only by h ignores the cost already paid, so it can chase cells that look close to G and waste effort on dead ends (or return a longer path in other mazes).
- On *this* maze, greedy would actually find the optimal 18-step path (along row 0, then down column 9), so this maze can't show the failure on its own.

**A\***
- Definitions, for a node `n`:
  - `g(n)`: the actual cost paid so far to get from the start to `n` (the number of steps taken, since every move costs 1).
  - `h(n)`: the heuristic, an *estimate* of the cost still to come from `n` to the goal. Here, the Manhattan distance from `n` to G.
  - `f(n) = g(n) + h(n)`: the estimated total cost of the best path from start to goal that passes through `n`. This is the heap priority.
- Priority = `f = g + h`: cost paid so far plus estimated cost remaining.
- Extreme cases: `h = 0` everywhere (no information) behaves like UCS/BFS on a unit-cost grid; `h =` exact remaining distance (including detours) means no wrong turns.
- Manhattan distance sits between these. My guess: closer to exact than to zero, so a reasonable saving over BFS. To be tested by experiment.

**Python notes**
- Generator expression + `next(...)` returns the first match; a plain loop is equivalent.
- A list of strings already works as a 2D grid (`maze[r][c]`). Convert to a list of lists only if I want to modify cells (e.g. overlaying the path when rendering).
- `yield` is lazy and one-shot; for at most 4 neighbours a returned list is just as good and avoids the "consumed once" trap.
- Type hints use subscripts: `def neighbours(r: int, c: int) -> list[tuple[int, int]]:` (not `list(tuple)`).

## Next steps
1. Finish `solution.py` scaffolding: `start`, `goal`, `neighbours`.
2. Write `bfs()`, returning the path and the set of expanded cells. Define "expanded" once (e.g. cells popped from the queue) and use the same definition for A*.
3. Record BFS path length (expected 18) and expanded count.
4. Implement A* with `heapq`, priority `f = g + h`, h = Manhattan distance. Decide how to handle tie-breaking and cells reached by a cheaper route later.
5. Confirm the same path length; compare expanded counts against BFS.
6. Render both searches (expanded cells marked, path overlaid) and compare the shapes: BFS diamond vs A* narrower corridor toward G.
7. Optional extension: h = 3 x Manhattan (inadmissible): faster? still optimal? Find a maze where it is suboptimal. Then add diagonal moves at cost sqrt(2) and switch to octile distance.
