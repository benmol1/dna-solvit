# Eigenvectors & PageRank: Notes (in progress)

**Setup:** a six-page web (A to F). The aim is to score each page's importance using only who links to whom.

## Why counting inbound links isn't enough

The simplest score is the number of inbound links: a page that is referenced a lot is likely to be useful. But every link counts equally and links are free to make, so a spammer can create 1,000 dummy pages that all link to one target.

## The random surfer

A surfer sits on a page, picks one of its outgoing links uniformly at random, follows it, and repeats. This is a Markov chain, and a page's score is its probability in the **stationary distribution**: the long-run chance of finding the surfer there.

- Pages that are never revisited (**transient** states), such as dummies that nobody links to, score zero in the long run.
- Their starting probability still has to go somewhere. If 1,000 of 2,000 pages are dummies linking only to the target, half of a uniform start moves to the target on the first step.

## Traps and link farms

If the target links back to the dummies, and nothing links out of that group, the surfer can get in but never leave. This is a **link farm**.

Our web has a trap by accident: A, B and C only link to each other. Without any fix, the surfer ends up cycling among them, and D, E and F score exactly zero. F → E → D can delay the surfer, but the probability of still being outside the trap decays to nothing.

## Damping (teleporting)

First idea: when the surfer notices a loop, restart on a random page. Noticing a loop needs a memory of where the surfer has been, so it would no longer be a simple Markov chain on six states.

The memoryless version, at every step:

- with probability `d` = 0.85, follow a random link from the current page;
- with probability `1 - d`, jump to a page chosen from all six (possibly the current one).

Every page can now be reached from every other in one step, so no group can hold the surfer for ever. The update is:

    new[p] = d * sum(rank[q] / outdegree(q) for each q linking to p) + (1 - d) / 6

For A on the first step, with links from C (outdegree 1) and D (outdegree 2):

    d * (1/6 + 1/6 * 1/2) + (1 - d) / 6

## Implementation (`solution.py`)

Start every page at 1/6 and apply the update until no rank changes by 1e-10 or more.

Things I got wrong on the way:

- Looping over a dictionary gives its **keys**. `q` is just a page name, and its outgoing links are `links[q]`.
- Each term in the sum uses the rank of the **sending** page `q`: the probability of being on `q` times the probability of picking the link to `p`. I had multiplied the whole sum by the receiving page's rank instead.
- **Sanity check:** the ranks are probabilities, so they should sum to 1 after every iteration (up to rounding). With my bug they didn't.

## Result

Converged after **44 iterations**:

| page | rank |
|---|---|
| C | 0.37 |
| A | 0.36 |
| B | 0.18 |
| D | 0.040 |
| E | 0.036 |
| F | 0.025 |

The order matches my prediction, made before running it: C, A, B, D, E, F.

## Interpreting the result (is in-link count the whole story?)

No. With d = 0.999 (almost no teleporting) the ranks were C 0.40, A 0.40, B 0.20, and D, E, F about 0.0003 or less (65 iterations).

- Inside the trap A, B, C: C has two in-links from the trio and A only one, yet they tie. Every visit to C is followed by a visit to A, and from A the surfer goes to C or B with probability ½ each. That gives visit ratios A : C : B = 1 : 1 : ½, which scale to 0.4 : 0.4 : 0.2.
- The same facts as balance conditions: A = C, B = A/2, C = A/2 + B. The steady state is the vector that the update leaves unchanged.
- A page with no in-links still scores `(1 - d) / n` from teleporting alone. F = 0.001/6 ≈ 0.000167, as observed.
- The tail then builds up along the chain F → E → D: E ≈ F + ½F = 1.5F and D ≈ F + ½E = 1.75F (when d is close to 1). These match the output.
- A vote is worth more when it comes from a well-ranked page, and A's single strong in-link from C is worth more than many weak ones.
- `problem.md` says A has "only one inbound link", but in `links` A is linked from both C and D. Only inside the trap does A have a single in-link.

## Matrix form (power iteration)

Build `M` with `M[p][q] = 1 / outdegree(q)` if `q` links to `p`, else 0. Each column then sums to 1 (it's a probability distribution over where the surfer goes next). The update becomes

    rank = d * (M @ rank) + (1 - d) / n

repeated until the change is below 1e-10. This is power iteration and gives the same ranking as the loops.

Three ways to solve it in `solution.py`'s `pagerank_matrix(method=...)`:

- `"power"`: iterate the update above.
- `"inverse"`: the fixed point satisfies `(I - dM) rank = (1 - d)/n`, so solve it directly with `np.linalg.inv`. This is a linear solve, not an eigenvalue method, and I had misnamed the flag at first.
- `"eig"`: fold the teleporting into `G = d*M + (1 - d)/n * ones`, call `np.linalg.eig`, take the eigenvector with the largest eigenvalue and divide by its sum (which also fixes the sign). Every column of `G` sums to 1, so the largest eigenvalue is exactly 1, and the other eigenvalues have magnitude at most d.

## Performance (random web, n = 2,000, 5 out-links per page, d = 0.85)

| method | time |
|---|---|
| basic dictionary loops | about 6.7 s |
| power iteration | 9.4 ms |
| matrix inverse | 185 ms |
| `np.linalg.eig` | 7.48 s |

What I learned:

- **Building `M` can dominate.** My first version looped over all n² (row, column) pairs and did a list scan for each, which took about 700 ms and made the algorithms look as if they were close. Looping only over the actual links took about 8 ms.
- **Time the pieces separately.** Splitting build from solve showed that the first comparison was measuring the setup, not the algorithms.
- **Big-O hides constants.** Inversion and `eig` are both O(n³), yet `eig` was about 40× slower than the inverse. It computes all n eigenpairs of a non-symmetric matrix, with complex arithmetic, when we need one.
- **Power iteration wins.** One step costs about n² dense (or the number of links when sparse), and the number of steps depends on d and the tolerance, not on n. The error shrinks by about a factor d per step: 44 iterations at d = 0.85 and 65 at d = 0.999.
- **My prediction was wrong.** I expected the "eigenvalue" (inversion) method to be quickest on a large web. It is the slowest of the sensible choices.

## What production systems do

They use power iteration (an eigenvector method) on a **sparse** matrix. The dense `M` has n² entries, but each page has only a handful of links, so almost all of them are zero. At n = 20,000 a dense float64 matrix is 3.2 GB, and the inversion needs several copies of it. A sparse format (e.g. `scipy.sparse`) stores only the non-zeros, so memory is proportional to the number of links, and `M @ rank` costs about the number of links too. Inversion can't use sparsity, because the inverse of a sparse matrix is generally dense. I haven't implemented or timed the sparse version yet, so the time saving is an expectation, not a measurement.

## Next

1. Switch `M` to a sparse matrix and measure memory and time on a large web.
2. Extension: add a page G with no outgoing links (a **dangling page**) and fix the algorithm. Its column in `M` is all zeros, so the column doesn't sum to 1 and rank leaks away. The standard trick is to let G link to every page.
