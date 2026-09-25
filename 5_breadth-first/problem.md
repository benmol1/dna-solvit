# Breadth-First Search

Two words are connected if they differ in exactly one letter. Using only this dictionary:

words = ["cold","cord","card","ward","warm","wart","cart","core","care",
 "bare","bore","born","corn","cost","cast","case","cave","code",
 "mode","made","mare","more","wore","word","wood","good","gold",
 "goad","load","lead","dead","deal","heal","heat","head"]

 - Build the graph. Think about how to find neighbours efficiently, comparing every pair is O(n²·L); there's a neat trick with wildcard buckets like c_ld that's O(n·L).

 - Implement BFS to find a shortest ladder from cold to warm, returning the actual path (you'll need to track parents).

 - Swap the queue for a stack, rerun, and compare the path you get. Explain what changed and why.

## Extension
Load /usr/share/dict/words (on macOS), filter to 4-letter lowercase words, and find the longest shortest-path in the graph, the hardest ladder in English. Then implement bidirectional BFS and measure how many fewer nodes it visits.

## Tutor instruction
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

## Solution
Shortest ladder is 4 steps (5 words), e.g. cold → cord → word → ward → warm. (Verified by BFS over this exact list; other 4-step paths may exist and are equally correct.)