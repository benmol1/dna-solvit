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
- `neighbours(current)` fails when `current` is a `(row, col)` tuple but the function takes two arguments. Fix: call `neighbours(*current)`, or make the function take one `pos` tuple and unpack inside.
- Don't reuse the function's name for a local variable inside it (shadowing); use something like `result`.
- Use `collections.deque` for the BFS queue: `deque([start])`, `queue.popleft()`, `queue.append(...)`. `list.pop(0)` shifts every element, so it's slow on big queues. Note `deque(start)` would be a bug (it iterates the tuple).
- Rendering: strings are immutable, so `render(path, expanded)` converts each row to a list of characters, marks expanded cells (`o`) then path cells (`*`) on `.` cells only (so `S`, `G`, `#` stay visible), and joins back to strings.
- Colour in the terminal: `rich`, `colorama` or `termcolor`, or plain ANSI escape codes (e.g. `"\033[92m" + text + "\033[0m"`), which work on Windows 11 terminals with no extra dependency. Adding a package would mean `uv add ...` and changing `pyproject.toml`.

## Results so far
- BFS finds a path of **18 steps**, matching the reference.
- The BFS path went along row 0 to column 5, down to row 2, along to column 9, then down column 9. The route along all of row 0 and down column 9 is also 18 steps. So there are **multiple optimal paths**, and which one comes out depends on tie-breaking (neighbour order and FIFO queue order). A* may pick a different one, so compare path *length* and *expanded counts*, not exact cells.

## Visited vs expanded
- `visited` (as written) is updated when a cell is **discovered**, i.e. pushed onto the queue.
- **Expanded** means popped from the queue and its neighbours examined.
- When the loop stops on the goal, the queue is usually non-empty, so `visited` = expanded + the frontier at that moment. They are not the same set.
- Open question to settle: which count is the fairer measure of "work done" when comparing BFS and A*? Either is fine if used consistently, but think about which best matches the work the search actually did. Check with `print(len(visited), len(queue))` at the end of `bfs()`.

## Next steps
1. Finish `solution.py` scaffolding: `start`, `goal`, `neighbours` (done).
2. Make `bfs()` return the path and the set of expanded cells. Define "expanded" once (cells popped from the queue) and use the same definition for A*. (Basic BFS with path is done; expanded tracking still to do.)
3. Record BFS expanded count (before running, predict it out of the 100 cells).
4. Implement A* with `heapq`, priority `f = g + h`, h = Manhattan distance. Decide how to handle tie-breaking and cells reached by a cheaper route later.
5. Confirm the same path length; compare expanded counts against BFS.
6. Render both searches (expanded cells marked, path overlaid) and compare the shapes: BFS diamond vs A* narrower corridor toward G.
7. Optional extension: h = 3 x Manhattan (inadmissible): faster? still optimal? Find a maze where it is suboptimal. Then add diagonal moves at cost sqrt(2) and switch to octile distance.
