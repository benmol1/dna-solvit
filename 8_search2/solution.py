from collections import deque

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
    
    neighbours = []

    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
            neighbours.append((nr, nc))

    return(neighbours)


def bfs():
    # return (path, expanded) where expanded is the set of cells you popped
    print(list(neighbours(0, 0)))   # try this
    print(list(neighbours(1, 0)))   # and this, then compare with the maze

    print(f"done")
    return()


def main():
    bfs()


if __name__ == "__main__":
    main()