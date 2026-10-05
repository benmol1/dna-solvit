from collections import deque
from rich.text import Text
from rich.console import Console




maze = ["S.........",
        ".####.###.",
        ".#........",
        ".#.######.",
        ".#.#....#.",
        "...#.##.#.",
        "####.##.#.",
        ".....#..#.",
        ".#####.##.",
        ".........G"]

rows, cols = len(maze), len(maze[0])
for r, row in enumerate(maze):
    if "S" in row:
        start = (r, row.index("S"))
    if "G" in row:
        goal = (r, row.index("G"))


def neighbours(r: int, c: int) -> list[tuple]:
    
    result = []

    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
            result.append((nr, nc))

    return(result)


def get_path_from_parents(source, destination, parents):
    hop_dest = destination
    hop_source = ""
    path = []
    length = 0

    while hop_source != source:
        path.append(hop_dest)
        hop_source = parents[hop_dest]
        length += 1
        hop_dest = hop_source

    path.append(source)
    path.reverse()
    return path, length


def render(path, expanded=()):
    grid = [list(row) for row in maze]

    for r, c in expanded:
        if grid[r][c] == ".":
            grid[r][c] = "o"

    for r, c in path:
        if grid[r][c] == ".":
            grid[r][c] = "*"

    return ["".join(row) for row in grid]






def bfs():
    # return (path, expanded) where expanded is the set of cells you popped
    queue = deque([start])
    visited = {start}
    parents = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbour in neighbours(*current):
            if neighbour not in visited:
                visited.add(neighbour)
                parents[neighbour] = current
                queue.append(neighbour)

    return(get_path_from_parents(start, goal, parents))


def main():

    # Initialise console for colour printing
    console = Console()
    styles = {"*": "bold green", "o": "grey50", "S": "yellow", "G": "yellow", "#": "blue"}

    # Run the Breadth-First Search
    path, length = bfs()
    print(f"BFS: length={length}")
    print(f"Path: {path}")

    # Print to console
    for line in render(path):
        t = Text()
        for ch in line:
            t.append(ch, style=styles.get(ch, ""))
        console.print(t)


if __name__ == "__main__":
    main()