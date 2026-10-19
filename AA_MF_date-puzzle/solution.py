import sys
import time
from datetime import date, datetime
from rich.console import Console
from rich.text import Text

# The DragonFjord "A-Puzzle-A-Day" board. None marks a square outside the board.
board_labels = [
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", None],
    ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", None],
    ["1",   "2",   "3",   "4",   "5",   "6",   "7"],
    ["8",   "9",   "10",  "11",  "12",  "13",  "14"],
    ["15",  "16",  "17",  "18",  "19",  "20",  "21"],
    ["22",  "23",  "24",  "25",  "26",  "27",  "28"],
    ["29",  "30",  "31",  None,  None,  None,  None],
]

# The eight pieces, drawn as they lie in the photo. 41 squares in total,
# so placing all of them on the 43-square board leaves exactly two uncovered.
pieces = {
    "yellow":     ["XXX",
                   "XXX"],
    "orange":     ["XX",
                   "XX",
                   "X."],
    "sky":        [".X",
                   "XX",
                   ".X",
                   ".X"],
    "magenta":    ["XXX",
                   "X.X"],
    "blue":       [".XXX",
                   "XX.."],
    "lime":       ["..X",
                   "XXX",
                   "X.."],
    "red":        ["X...",
                   "XXXX"],
    "green":      ["..X",
                   "..X",
                   "XXX"],
}

colours = {
    "yellow": "yellow1", "orange": "dark_orange", "sky": "deep_sky_blue1",
    "magenta": "deep_pink3", "blue": "blue3", "lime": "green1",
    "red": "red3", "green": "spring_green4",
}


def cells_from_drawing(drawing):
    return [(r, c) for r, row in enumerate(drawing) for c, ch in enumerate(row) if ch == "X"]


def normalise(cells):
    # Shift so the smallest row and column are 0, and sort so equal shapes compare equal
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def get_orientations(cells):
    # All rotations, each with and without a flip; duplicates removed (the rectangle has only 2)
    orientations = set()
    shape = cells
    for _ in range(4):
        shape = [(c, -r) for r, c in shape]  # rotate 90 degrees
        orientations.add(normalise(shape))
        orientations.add(normalise([(r, -c) for r, c in shape]))  # mirror image
    return sorted(orientations)


def find_label(label):
    for r, row in enumerate(board_labels):
        for c, value in enumerate(row):
            if value == label:
                return (r, c)
    raise ValueError(f"No square labelled {label!r}")


def solve(month, day, find_all=False):
    # grid[r][c] is None for off-board squares, "date" for the squares we must leave showing,
    # "" for empty squares, and a piece name once covered
    grid = [["" if label is not None else None for label in row] for row in board_labels]
    for r, c in (find_label(month), find_label(str(day))):
        grid[r][c] = "date"

    orientations = {name: get_orientations(cells_from_drawing(d)) for name, d in pieces.items()}
    unused = list(pieces)
    solutions = []
    placements = 0

    def first_empty():
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if value == "":
                    return (r, c)
        return None

    def fits(cells):
        return all(0 <= r < 7 and 0 <= c < 7 and grid[r][c] == "" for r, c in cells)

    def place_shape(name, cells):
        for r, c in cells:
            grid[r][c] = name

    def remove_shape(cells):
        for r, c in cells:
            grid[r][c] = ""

    def search():
        nonlocal placements
        target = first_empty()
        if target is None:
            solutions.append([row[:] for row in grid])
            return not find_all  # True means "stop searching"

        # The first empty square (in reading order) must be covered by some piece. For each
        # orientation, the square it covers must be the orientation's own first square:
        # any earlier square of the piece would land on a square that is already filled.
        for name in list(unused):
            for shape in orientations[name]:
                anchor_r, anchor_c = shape[0]
                cells = [(target[0] + r - anchor_r, target[1] + c - anchor_c) for r, c in shape]

                # If the shape does not fit here, try the next orientation/shape
                if not fits(cells):
                    continue

                # If the shape does fit here, place it on the grid
                placements += 1
                place_shape(name, cells)
                unused.remove(name)

                # Search for solutions on this branch given the shape we've just placed. Will only
                # return True if there is a solution on this branch (and find_all=False)
                if search():
                    return True

                # If there is not a solution on this branch, remove the shape we just placed and
                # try again with the next orientation/shape
                remove_shape(cells)
                unused.append(name)
        return False

    search()
    return solutions, placements


def render(solution):
    text = Text()
    for r, row in enumerate(solution):
        for c, value in enumerate(row):
            if value is None:
                text.append("     ")
            elif value == "date":
                text.append(f"{board_labels[r][c]:^5}", style="bold white on grey11")
            else:
                # The piece's initial as well as its colour, so it still reads without colour
                text.append(f"  {value[0].upper()}  ", style=f"black on {colours[value]}")
        text.append("\n")
    return text


def parse_date(args):
    # Accepts nothing (today), "17 Oct", "Oct 17" or "2026-10-17"
    if not args:
        d = date.today()
    elif len(args) == 1:
        d = datetime.strptime(args[0], "%Y-%m-%d").date()
    else:
        day, month = (args[0], args[1]) if args[0].isdigit() else (args[1], args[0])
        d = datetime.strptime(f"2024 {month[:3].title()} {int(day)}", "%Y %b %d").date()  # 2024: allow 29 Feb
    return d.strftime("%b"), d.day


def main():
    args = sys.argv[1:]
    find_all = "--all" in args
    args = [a for a in args if a != "--all"]
    month, day = parse_date(args)

    start = time.perf_counter()
    solutions, placements = solve(month, day, find_all=find_all)
    elapsed = time.perf_counter() - start

    console = Console()
    console.print(f"[bold]{day} {month}[/bold]: {len(solutions)} solution(s), "
                  f"{placements:,} placements tried, {elapsed:.2f}s\n")
    if solutions:
        console.print(render(solutions[0]))


if __name__ == "__main__":
    main()
