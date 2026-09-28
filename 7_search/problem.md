# Uniform-Cost & Bidirectional Search

## Problem - part 1, the Romania map (city: {neighbour: km}):

roads = {"Arad":{"Zerind":75,"Sibiu":140,"Timisoara":118},
 "Zerind":{"Arad":75,"Oradea":71}, "Oradea":{"Zerind":71,"Sibiu":151},
 "Sibiu":{"Arad":140,"Oradea":151,"Fagaras":99,"RimnicuVilcea":80},
 "Timisoara":{"Arad":118,"Lugoj":111}, "Lugoj":{"Timisoara":111,"Mehadia":70},
 "Mehadia":{"Lugoj":70,"Drobeta":75}, "Drobeta":{"Mehadia":75,"Craiova":120},
 "Craiova":{"Drobeta":120,"RimnicuVilcea":146,"Pitesti":138},
 "RimnicuVilcea":{"Sibiu":80,"Craiova":146,"Pitesti":97},
 "Fagaras":{"Sibiu":99,"Bucharest":211},
 "Pitesti":{"RimnicuVilcea":97,"Craiova":138,"Bucharest":101},
 "Bucharest":{"Fagaras":211,"Pitesti":101,"Giurgiu":90,"Urziceni":85},
 "Giurgiu":{"Bucharest":90}, "Urziceni":{"Bucharest":85,"Hirsova":98,"Vaslui":142},
 "Hirsova":{"Urziceni":98,"Eforie":86}, "Eforie":{"Hirsova":86},
 "Vaslui":{"Urziceni":142,"Iasi":92}, "Iasi":{"Vaslui":92,"Neamt":87},
 "Neamt":{"Iasi":87}}

 - Implement uniform-cost search with heapq, tracking parents. Find the cheapest Arad → Bucharest route and its cost. Before running: eyeball the map and commit to a guess.

 - Implement greedy "always take the edge toward the fewest-hops route": BFS by hop count. What route does it find, and how much worse is it?

 ## Problem - part 2
 Meet in the middle, on the 8-puzzle instance start=(7,2,4,5,0,6,8,3,1), goal=(0,1,2,3,4,5,6,7,8):

 - Implement bidirectional BFS: two frontiers, two visited-with-depth dicts, alternate expanding the smaller frontier level by level; stop when a newly generated state appears in the other side's dict, and stitch the move count together.

 - Confirm the optimal length is 26 moves, and compare nodes expanded. Explain the b^(d) versus 2b^(d/2) arithmetic to your tutor, then check it roughly predicts your measured ratio.

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