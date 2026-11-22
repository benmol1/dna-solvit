# Genetic Algorithms: Knapsack — Notes (in progress)

**Setup:** 25 items with weights and values, capacity 100. Choose the subset with the highest total value whose weight stays within capacity. This is the **0/1 knapsack**: each item is taken whole or not at all. The DP optimum is 402, per problem.md, and my own `knapsack_dp` now reproduces it.

## Encoding

A candidate packing is a 25-bit string, and bit *i* = 1 means item *i* is packed. There are 2²⁵ ≈ 33.5 million candidates, and the count doubles with every extra item. Brute force works at 25 items but not at 50 or 100.

## Greedy by value density

Sort by value ÷ weight and pack in that order, skipping any item that no longer fits. It gets **398 against the optimum of 402**.

- With *fractional* items this strategy is provably optimal. The 0/1 version loses because of **trapped capacity**: leftover room that no remaining item fits into.
- A better packing can leave out a high-density item so that two medium items fit together more efficiently. Greedy commits in order and can never make that trade.
- So 398 is the baseline the GA has to match or beat.

## Most random packings are infeasible

A random bit-string includes each item with probability ½, so its expected weight is half the total weight: 408 / 2 = **204 kg**, about double the 100 kg capacity. Sampling 100,000 random bit-strings gave **only ~1.4% under the limit**.

Consequence: a random starting population of 100 has only about 1–2 feasible individuals. The GA has to deal with overweight individuals from generation 0. The two approaches the problem asks for:

- **Penalise:** keep infeasible individuals, but reduce their fitness.
- **Repair:** drop random items until the bag fits.

Open design question for next time: how strong should the penalty be? Too gentle and the population drifts towards overweight bags with high value. Too harsh (e.g. fitness 0) and the ~98 infeasible individuals in generation 0 all look identical, so selection has nothing to work with.

## Exact solution: DP over capacities

`best[c]` = the highest total value achievable in a bag of capacity `c`, using only the items considered so far. It starts as all zeros (no items, so every bag is worth 0).

For each item (w, v) and each capacity `c >= w`, there are two options:

- **Leave it out:** `best[c]` (unchanged).
- **Put it in:** `v + best[c - w]`, which is the item's value plus the best use of the leftover capacity.

Take the max: `best_new[c] = max(best[c], best[c - w] + v)`. After all 25 items, `best[100]` is the optimum, **402**. The cost is O(items × capacity), compared with 2²⁵ for brute force.

- **Why `best_new`:** `best[c - w]` must be the value from *before* this item, otherwise the item could be counted twice. I used a separate `best_new` list for this.
- **Open question (not yet worked out):** updating in place instead needs `c` to loop **descending**, not ascending, for the same reason. Ascending would let the item be reused (the unbounded knapsack). My first guess was ascending, which was wrong. Worth testing on one item (w=4, v=59) to see `best[8]` come out as 118 instead of 59.

## Fitness: linear penalty

`fitness_linear(bits, alpha) = value - alpha * max(0, weight - CAPACITY)`. Fitness 0 for every overweight bag is too harsh because a 1 kg overweight bag and a 150 kg overweight bag look the same. Scaling the penalty with the overage fixes that.

`alpha` is an **exchange rate between kg over the limit and value**. Dropping an item from an overweight bag is a net gain if `alpha` × (kg of overage it removes) is bigger than the item's value.

- Break-even for a junk item (w=29, v=1) in a bag 10 kg over: `alpha ≈ 0.1`.
- Break-even for a great item (w=4, v=59): `alpha ≈ 15` (59/4).
- Value per kg ranges up to 24. If `alpha` exceeds the density of every item, overweight bags can never beat feasible ones. That behaves almost like the "0 for all overweight" rule (tested with `alpha = 10`).
- A small `alpha` such as 0.5 makes overweight bags attractive: the population drifts overweight. Note that break-even is `extra_value = alpha × extra_kg`, so at `alpha = 0.5` the bag needs only *half* a value point per extra kg, not double.
- The penalty only counts kg *over capacity*. Shedding weight beyond that earns nothing.

`plot_fitness_histogram(fits, filename, title)` saves a PNG of the fitness distribution next to the script. At generation 0 most bags are infeasible, so the histogram is mostly negative or low values for large `alpha`.

## GA building blocks (in `solution.py`)

- **Generation:** one round of score, select parents, make children, replace the population. Run 200 of them.
- **Tournament selection** (`tournament`): sample `k` individuals, take the best. The best individual enters a tournament with probability `k/100` and always wins it. `k = 1` is random selection (maximum diversity, no progress). `k = 100` always picks the single best (no diversity, children are clones). Typical: `k = 2` to `5`.
- **One-point crossover** (`crossover`): `p1[:cutoff] + p2[cutoff:]`. `cutoff` of 0 or 25 copies one parent, so useful cutoffs are 1 to 24. **Currently fixed at 13, which is a known weakness:** bits 0 to 12 always travel together, so crossover can never combine bit 3 from one parent with bit 10 from another. TODO: random cutoff.
- **Mutation** (`mutate`): flip each bit with probability 1/25. Expected flips per child = 1, and about 36% of children get none ((24/25)²⁵). It returns a new list, so parents are never modified.
- **`make_child`:** tournament for p1, and for p2 if crossover is on, then crossover, then mutate. `use_crossover=False` means the child is just a mutated tournament winner. A boolean switch is enough for the ablation.
- **`run_ga`:** copy the `n_elite` best individuals unchanged, then fill the rest with `make_child`. Returns best and mean fitness per generation.

## First GA runs (single run each, 100 individuals, 200 generations, k=2, 2 elites)

| alpha | gen 0 best | final best | final mean |
|---|---|---|---|
| 0.5 | 434 | 536 | 488 |
| 2 | 293 | 406 | 354 |
| 15 | 153 | 402 | 126 |

The DP optimum is 402, so a fitness above 402 must come from an **infeasible** bag whose penalty is too small. At `alpha = 0.5` and `2` the GA is exploiting the penalty. `best_hist` stores *penalised fitness*, not packed value, so it can't tell whether the best individual is legal.

- **Not yet understood:** why `alpha = 15` has a final best of exactly 402 but a mean of only 126.
- **Needed:** track the best *feasible* value and its weight separately from penalised fitness.

## Concepts so far

- **Hill climbing** (as I've implemented it): propose a move, keep it only if it improves.
- **Simulated annealing:** accept a worse move with probability exp(−Δ/T), cooling T over time.
- **Natural selection:** variation is blind and creates new candidates. Selection is the only part with direction.

## Next

1. ~~Fill in `knapsack_dp` and check it gives 402.~~ Done.
2. ~~Design the fitness function.~~ Penalty version done (`alpha`). Repair version (drop random items until the bag fits) not yet implemented.
3. ~~Build the GA pieces and generation loop.~~ Done (`run_ga`). Still to do: random crossover cutoff, track best *feasible* value, plot best and mean fitness per generation, 10 runs per setting.
4. Compare penalty against repair. Then sweep `alpha` and ask how reliably each reaches 402.
5. Ablations: no crossover, then no mutation.
6. Clean up: `genetic()` in `solution.py` is an unfinished stub that nothing calls.
