# A* Search — Notes

**Setup:** a 10×10 maze (`S` top-left, `G` bottom-right, `#` walls), moves up/down/left/right at cost 1. Goal: find the shortest path with BFS, then with A* (Manhattan heuristic, `heapq`), and compare how many nodes each *expands*.

## The idea

| Term | Meaning |
|---|---|
| `g(n)` | actual cost paid from the start to `n` (steps taken) |
| `h(n)` | heuristic: *estimated* cost still to come from `n` to the goal (here, Manhattan distance) |
| `f(n) = g(n) + h(n)` | estimated total cost of the best path through `n`; the heap priority |

- **BFS** orders by arrival, so it expands cells in order of `g`. It is optimal but blind to where `G` is: on an open grid its wavefront is a growing *diamond* centred on `S`.
- **Greedy** (order by `h` alone) is goal-seeking but ignores what has been paid, so it can chase cells that look close and waste effort on dead ends or return a longer path.
- **A\*** (order by `f = g + h`) combines both. With `h = 0` everywhere it reduces to BFS/UCS; with `h` equal to the exact remaining distance it never takes a wrong turn. Manhattan distance sits between.

**Why Manhattan is admissible:** walls can only make the true path *longer*, never shorter, so `h ≤ true remaining cost`. A heuristic that never overestimates is *admissible*, and that is what keeps A* optimal.

## Results

| Maze | Search | Path length | Expanded |
|---|---|---|---|
| Original | BFS | 18 | 36 |
| Original | A\*, heap entries `(f, cell)` | 18 | 31 |
| Original | A\*, heap entries `(f, h, cell)` | 18 | **19** |
| Open 10×10 | BFS | 18 | 100 |
| Open 10×10 | A\*, `(f, cell)` | 18 | 100 |
| Open 10×10 | A\*, `(f, h, cell)` | 18 | **19** |

(`expanded` = popped from the queue/heap and its neighbours examined. 19 is the minimum possible for an 18-step path: the 19 cells on the path itself.)

BFS on the original maze (`*` path, `o` expanded):

```
S*****oooo
o####*###o
o#ooo*****
o#o######*
o#o#....#*
ooo#.##.#*
####.##.#*
.....#..#*
.#####.##*
.........G
```

A\* with the `h` tie-break expands only the path:

```
S*********
.####.###*
.#.......*
.#.######*
.#.#....#*
...#.##.#*
####.##.#*
.....#..#*
.#####.##*
.........G
```

## What the numbers say

**Where the saving comes from.** A* expands cells in increasing `f`, so any cell with `f` above the true cost (18) is never expanded, because `G` (with `f = 18`) comes off the heap first. The branch `(2,2)`–`(2,4)` has `f = 24`, so A* ignores it. BFS expands it.

**Why the saving on the original maze is modest at first (31 vs 36).** Cells that lie on *any* down-or-right route have `f = 18` exactly: each step raises `g` by 1 and lowers `h` by 1. The whole left column, `(0,7)` and `(2,0)` are all tied with the optimal path, so A* has no reason to put them off. `S` is in the corner, so there is almost no "away from the goal" territory to prune.

**Ties matter more than expected.** On the open grid every cell has `f = 18`, so `f` can't distinguish anything. With heap entries `(f, cell)`, ties fall back to comparing `(row, col)`, which sweeps the grid row by row and expands all 100 cells, no better than BFS. Adding `h` as the second tuple element (`(f, h, cell)`) makes the heap prefer the cell closest to `G` among equals, and A* drops to the minimum of 19. Admissibility guarantees the path is optimal; tie-breaking decides how much work it takes to find it.

**The experiment is favourable to A\*.** The optimal route here only ever moves down or right, so `h` never misleads. A* helps most where the map forces moves *away* from `G` (`f` above the optimum), not just where there are dead ends: a dead end pointing toward `G` still has `f = 18` and gets explored.

## Implementation notes

- **`visited` vs `g`.** BFS can mark a cell visited the first time it is *discovered*, because its queue is ordered by distance and the first discovery is cheapest. In A* the heap is ordered by `f`, so a cell can be discovered by a more expensive route first. Instead, use `g` as the record: push a neighbour only if it is new or `g_new < g[neighbour]`, updating `g` and `parents` together.
- **Stale heap entries.** `heapq` can't remove or update an entry, so a cell may be pushed more than once. On pop, skip anything already in `expanded`.
- **Caveat on that skip.** It assumes a cell is never reached more cheaply *after* it has been expanded. That holds for a consistent heuristic like Manhattan distance on a unit-cost grid, but not necessarily for an inadmissible one (the `3 × Manhattan` extension).
- **Discovered ≠ expanded.** `len(g)` (cells reached) is `expanded` plus whatever is still on the frontier when the search stops. Compare `expanded` between searches, using the same definition for both.
- **Multiple optimal paths.** Tie-breaking decides *which* 18-step path comes out (BFS went via `(1,5)`, A* along row 0 and down column 9). Compare lengths and counts, not exact cells.

## Open questions / next steps

- Design a maze where A* with the `h` tie-break still expands nearly as many cells as BFS (walls that force the route away from `G`).
- Extension: `h = 3 × Manhattan` (inadmissible). Faster? Still optimal? Find a maze where it returns a longer path.
- Extension: diagonal moves at cost √2. Manhattan is now inadmissible, so switch to octile distance and re-verify optimality.
