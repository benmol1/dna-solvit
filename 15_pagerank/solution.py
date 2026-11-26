links = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["A", "C"],
    "E": ["C", "D"],
    "F": ["C", "E"],
}
d = 0.85
n = len(links)
rank = {page: 1 / n for page in links}
iterations = 0

while True:
    iterations += 1
    new = {}
    for p in links:
        inflow = 0
        for q in links:
            if p in links[q]:
                inflow += rank[q] / len(links[q])
        new[p] = (d * inflow) + (1 - d) / n

    change = max(abs(new[p] - rank[p]) for p in links)
    rank = new

    if change < 1e-10:
        break

print(f"Converged after {iterations} iterations")
for page, score in sorted(rank.items(), key=lambda kv: -kv[1]):
    print(page, f"{score:#.2g}")
