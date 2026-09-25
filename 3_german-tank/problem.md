# Estimation — the German Tank Problem

You capture four tanks with serial numbers 19, 40, 42, 60. Assume serials are 1..N, sampled without replacement, all equally likely.

 - Show by simulation that max(sample) is biased low: fix a true N (say 250) and k=4, simulate many captures, and plot the distribution of the max.

 - Design at least two better estimators. Candidates to consider: 2·mean − 1, and "max plus the average gap", i.e. max + max/k − 1.

 - Run a fair contest: for true N = 250, k = 4, compare your estimators' bias and RMSE over 100,000 simulated captures.

 - Give your estimate of N for the four captured serials above, using the winner.

## Extension 
Try a Bayesian version: put a prior on N (uniform on 60..1000), compute the posterior over N given the data, and report a 95% credible interval. Compare the posterior median to 74.

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

## Solution
The minimum-variance unbiased estimator is max + max/k − 1 = 60 + 60/4 − 1 = 74. Your simulation contest should show it beating both the raw max (biased low) and 2·mean − 1 (unbiased but higher variance).