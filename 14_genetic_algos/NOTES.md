# Genetic Algorithms: Knapsack — Notes (in progress)

**Setup:** 25 items with weights and values, capacity 100. Choose the subset with the highest total value whose weight stays within capacity. This is the **0/1 knapsack**: each item is taken whole or not at all. The DP optimum is 402, per problem.md (my own DP in `knapsack_dp` is still a stub).

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

## Concepts so far

- **Hill climbing** (as I've implemented it): propose a move, keep it only if it improves.
- **Simulated annealing:** accept a worse move with probability exp(−Δ/T), cooling T over time.
- **Natural selection:** variation is blind and creates new candidates. Selection is the only part with direction.

## Next

1. Fill in `knapsack_dp` and check it gives 402.
2. Design the fitness function (penalty vs repair).
3. Build the GA: tournament selection, one-point crossover, per-bit mutation ~1/25, elitism of 1–2. Population 100, 200 generations, 10 runs.
4. Ablations: no crossover, then no mutation.
