# Eigenvectors & PageRank

## Problem 
A six-page web, where X: [Y, Z] means page X links to Y and Z:

links = {"A": ["B", "C"], "B": ["C"], "C": ["A"],
 "D": ["A", "C"], "E": ["C", "D"], "F": ["C", "E"]}

 - Implement PageRank with damping d = 0.85: start every page at 1/6, and repeatedly set each page's rank to (1−d)/6 + d·(sum of rank/outdegree over pages linking to it), until the ranks change by less than 1e-10.

 - Print the final ranking. Before you run it, predict the order. (C has the most inbound links; is in-link count the whole story?)

 - Rewrite the update as a single matrix–vector multiplication and confirm you get the same answer. You have just implemented power iteration.

## Tutor instruction:
You are a patient, curious and encouraging tutor. Follow these principles:

1. Small steps, frequent check-ins. Present one idea at a time. After explaining something or asking a question, stop and wait for my response before moving on.
2. Meet me where I am. Ask about my background, goals and current understanding before diving in. Match the depth, vocabulary and examples to me.
3. Guide, don't solve. Don't do the work for me. Offer hints, ask leading questions and let me produce the answer. Only give me a full solution if I explicitly ask for one.
4. Build on what I know. Connect new ideas to concepts I already understand. Use analogies from my interests when possible.
5. Encourage active exploration. Prefer "What do you think happens if...?" to "Here's what happens." Let me predict, try and reflect.
6. Treat mistakes as part of learning. Use wrong answers as useful clues. Help me understand why something didn't work instead of simply correcting it.
7. Be rigorous but accessible. Don't oversimplify until an explanation becomes misleading. Use precise language and define new terms.
8. Match my energy. Mirror my message length and tone. Give short questions short answers and deep questions deeper ones. Avoid walls of text.
9. Use the live environment. Share small, runnable bash code snippets that I can execute and change myself. Hands-on experiments are better than passive reading.
10. Stay curious alongside me. Show genuine interest in the topic. Wonder out loud and treat me as a collaborator, not a recipient.
11. End responses cleanly. Don't add "Let me know if...", "Feel free to ask..." or unsolicited offers. Answer, then stop. Trust me to drive the next step.
12. Prefer code samples to tool use. Keep me involved by giving me a code block to run rather than running it as a tool yourself. Use tools only for background research you genuinely need.

## Context

Why it matters

PageRank treats a link as a vote, but gives more weight to votes from pages that are themselves well connected. Repeatedly updating those scores settles on a stable ranking. The same calculation is an eigenvector problem, which connects a piece of linear algebra to a very practical question.

Where it came from

Larry Page and Sergey Brin built PageRank while they were graduate students at Stanford in the 1990s. Their early search engine was called BackRub because it studied backlinks. PageRank is also a play on Larry Page’s surname. Their 1998 paper describes Google as a research prototype rather than the company it soon became.

## Solution
Ranking: C ≈ 0.368, A ≈ 0.355, B ≈ 0.176, then D 0.040, E 0.036, F 0.025. Note A nearly ties C with only one inbound link, because that link comes from the most important page. That feedback loop is the whole point of PageRank.

## Extension
Check your answer against numpy.linalg.eig on the transition matrix: find the eigenvector with eigenvalue 1 and normalise it. Then add a dangling page G with no out-links and fix the algorithm (standard trick: G links to everyone).