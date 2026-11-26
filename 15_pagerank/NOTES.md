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

## Next

1. Interpret the result. Is in-link count the whole story? Compare the size of the gaps between pages with their inbound links.
2. Rewrite the update as a single matrix–vector multiplication (a transition matrix times a probability vector) and confirm it gives the same answer. This is power iteration.
3. Extension: check against `numpy.linalg.eig` by finding the eigenvector with eigenvalue 1 and normalising it.
4. Extension: add a page G with no outgoing links (a **dangling page**) and fix the algorithm.
5. When reading the solution in `problem.md`, check what it says about A's inbound links against the `links` dictionary.
