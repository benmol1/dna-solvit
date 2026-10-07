import heapq
from collections import deque
from rich.console import Console
from rich.text import Text

maze_orig = [
    "S.........",
    ".####.###.",
    ".#........",
    ".#.######.",
    ".#.#....#.",
    "...#.##.#.",
    "####.##.#.",
    ".....#..#.",
    ".#####.##.",
    ".........G",
]

maze_empty = [
    "S.........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    ".........G",
]


def get_maze_properties(maze: list):
    rows, cols = len(maze), len(maze[0])
    for r, row in enumerate(maze):
        if "S" in row:
            start = (r, row.index("S"))
        if "G" in row:
            goal = (r, row.index("G"))

    return (rows, cols, start, goal)


def neighbours(maze, r: int, c: int) -> list[tuple[int, int]]:

    rows, cols = len(maze), len(maze[0])
    result = []

    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
            result.append((nr, nc))

    return result


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


def render(maze, path, expanded=()):
    grid = [list(row) for row in maze]

    for r, c in expanded:
        if grid[r][c] == ".":
            grid[r][c] = "o"

    for r, c in path:
        if grid[r][c] in [".", "o"]:
            grid[r][c] = "*"

    return ["".join(row) for row in grid]


def bfs(maze):

    _, _, start, goal = get_maze_properties(maze)

    # Initialise variables
    queue = deque([start])
    visited = {start}
    expanded = set()
    parents = {}

    # Loop through the queue. First-in, first-out
    while queue:
        current = queue.popleft()
        expanded.add(current)

        # If we have reached the goal, stop
        if current == goal:
            break

        # Check each neighbour. If we have not visited already, add to queue
        for neighbour in neighbours(maze, *current):
            if neighbour not in visited:
                visited.add(neighbour)
                parents[neighbour] = current
                queue.append(neighbour)

    path, length = get_path_from_parents(start, goal, parents)
    return (path, length, expanded)


def m_dist(a: tuple, b: tuple):
    return sum(abs(x - y) for x, y in zip(a, b))


def astar_search(maze):

    _, _, start, goal = get_maze_properties(maze)

    # Initialise variables
    expanded = set()
    parents = {}
    g = {start: 0}

    # Compute h (the manhattan distance to goal) and f for the start point
    h_start = m_dist(start, goal)
    f_start = g[start] + h_start

    # Add the start to the queue
    queue = [(f_start, h_start, start)]

    # Loop through the queue, popping in priority order. The priority is f = g + h, with h as the tiebreaker
    while queue:
        _, _, current = heapq.heappop(queue)

        # If we have already expanded this point then we don't need to do so again
        if current in expanded:
            continue
        expanded.add(current)

        # Stop if we have reached the goal
        if current == goal:
            break

        # Try each of the neighbours for this point. If the neighbour is unvisited (not in g)
        # or we've found a more efficient route to this neighbour, add to queue
        for neighbour in neighbours(maze, *current):
            g_new = g[current] + 1
            if (neighbour not in g) or (g_new < g[neighbour]):
                parents[neighbour] = current
                g[neighbour] = g_new

                h_neighbour = m_dist(neighbour, goal)
                f_neighbour = g[neighbour] + h_neighbour
                heapq.heappush(queue, (f_neighbour, h_neighbour, neighbour))

    path, length = get_path_from_parents(start, goal, parents)
    return (path, length, expanded)


def print_maze(console, lines, styles):
    for line in lines:
        t = Text()
        for ch in line:
            t.append(ch, style=styles.get(ch, ""))
        console.print(t)


def main():

    # Initialise console for colour printing
    console = Console()
    styles = {
        "*": "bold green",
        "o": "grey50",
        "S": "yellow",
        "G": "yellow",
        "#": "blue",
    }

    # Run the BFS Search
    path_bfs, length_bfs, expanded_bfs = bfs(maze_orig)
    print(f"BFS Search:\tlength: {length_bfs}, expanded: {len(expanded_bfs)}")

    # Render the BFS search
    print_maze(console, render(maze_orig, path_bfs, expanded_bfs), styles)

    # Run the A* Search
    path_astar, length_astar, expanded_astar = astar_search(maze_orig)
    print(f"\nA* Search:\tlength: {length_astar}, expanded: {len(expanded_astar)}")

    # Render the A* search
    print_maze(console, render(maze_orig, path_astar, expanded_astar), styles)


if __name__ == "__main__":
    main()
