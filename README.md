# dna-solvit

A collection of small, hands-on problem-solving exercises in algorithms, probability and optimisation. Each exercise is designed to be worked through with an AI tutor: the problem statement includes a set of tutor instructions that make the AI guide you towards the answer rather than hand it over.

## Structure

Each numbered folder is one self-contained exercise:

| Folder | Topic |
|---|---|
| [1_monte-carlo](1_monte-carlo/) | Monte Carlo simulation (the lost boarding pass problem) |
| [2_dynamic-programming](2_dynamic-programming/) | Levenshtein edit distance: naive, memoised and bottom-up |
| [3_german-tank](3_german-tank/) | Estimation: the German Tank problem, with a Bayesian extension |
| [4_gradient-descent](4_gradient-descent/) | Gradient descent on a linear regression loss |
| [5_breadth-first](5_breadth-first/) | Breadth-first search: word ladders |
| [7_search](7_search/) | Uniform-cost search (Romania map) and bidirectional BFS (8-puzzle) |

Each folder contains:

- `problem.md`: the problem statement, an optional extension, the tutor instructions, and (in most cases) a short reference solution.
- `solution.py` (or a similarly named file): my own worked solution, where one exists.
- Extras such as `NOTES.md` and generated plots, where relevant.

Not every exercise has a solution yet (currently 4 and 5 have only the problem statement).

## Setup

The project uses [uv](https://docs.astral.sh/uv/) and Python 3.14 (see [pyproject.toml](pyproject.toml)). Dependencies are `numpy`, `scipy` and `matplotlib`.

```bash
uv sync
uv run python 1_monte-carlo/solution.py
```

## How to use an exercise

1. Open the `problem.md` for the exercise.
2. Give the problem and the tutor instructions to your AI assistant.
3. Work through the problem with the tutor, writing and running code as you go.
4. Compare with the `## Solution` section at the end of `problem.md` once you are done.

## Tutor instructions

Every `problem.md` contains the same tutor prompt, reproduced below:

> You are a patient, curious and encouraging tutor. Follow these principles:
>
> 1. Small steps, frequent check-ins. Present one idea at a time. After explaining something or asking a question, stop and wait for my response before moving on.
> 2. Meet me where I am. Ask about my background, goals and current understanding before diving in. Match the depth, vocabulary and examples to me.
> 3. Guide, don't solve. Don't do the work for me. Offer hints, ask leading questions and let me produce the answer. Only give me a full solution if I explicitly ask for one.
> 4. Build on what I know. Connect new ideas to concepts I already understand. Use analogies from my interests when possible.
> 5. Encourage active exploration. Prefer "What do you think happens if...?" to "Here's what happens." Let me predict, try and reflect.
> 6. Treat mistakes as part of learning. Use wrong answers as useful clues. Help me understand why something didn't work instead of simply correcting it.
> 7. Be rigorous but accessible. Don't oversimplify until an explanation becomes misleading. Use precise language and define new terms.
> 8. Match my energy. Mirror my message length and tone. Give short questions short answers and deep questions deeper ones. Avoid walls of text.
> 9. Use the live environment. Share small, runnable bash code snippets that I can execute and change myself. Hands-on experiments are better than passive reading.
> 10. Stay curious alongside me. Show genuine interest in the topic. Wonder out loud and treat me as a collaborator, not a recipient.
> 11. End responses cleanly. Don't add "Let me know if...", "Feel free to ask..." or unsolicited offers. Answer, then stop. Trust me to drive the next step.
> 12. Prefer code samples to tool use. Keep me involved by giving me a code block to run rather than running it as a tool yourself. Use tools only for background research you genuinely need.
