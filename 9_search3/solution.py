
import random
import heapq

goal  = (0,1,2,3,4,5,6,7,8)
state = (7,2,4,5,0,6,8,3,1)

def get_neighbours(state):
    neighbours = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)

    moves = []
    if row > 0: moves.append(-3)
    if row < 2: moves.append(3)
    if col > 0: moves.append(-1)
    if col < 2: moves.append(1)

    for move in moves:
        new_index = zero_index + move

        s_list = list(state)
        s_list[zero_index], s_list[new_index] = s_list[new_index], s_list[zero_index]
        new_state = tuple(s_list)

        neighbours.append(new_state)

    return neighbours

def random_solvable_state(num_moves=100):

    state = goal
    for ii in range(num_moves):
        neighbours = get_neighbours(state)
        choice = random.choice(neighbours)
        state = choice

    return state

def md(state, include_blank=False):
    total_distance = 0
    for ii, tile_value in enumerate(state):
        if tile_value == 0 and not include_blank:
            continue
        goal_index = goal.index(tile_value)
        current_row, current_col = ii // 3, ii % 3
        goal_row, goal_col = goal_index // 3, goal_index % 3
        total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return total_distance


def misplaced_tiles(state, include_blank=False):
    result = 0

    for tile, goal_tile in zip(state, goal):
        if tile != goal_tile and (tile !=0 or include_blank):
            result += 1

    return result

def assert_md_dominates_mp():
    dominant_count = 0
    equal_count = 0
    for jj in range(1000):
        random_state = random_solvable_state()
        md_value = md(random_state)
        mp_value = misplaced_tiles(random_state)
        if md_value >= mp_value: dominant_count+=1
        if md_value == mp_value: equal_count+=1

    print(f"dominant_count: {dominant_count}, equal_count: {equal_count}")


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

def astar_search(h_function=md):

    start = state

    # Initialise variables
    expanded = set()
    parents = {}
    g = {start: 0}

    # Compute h and f for the start point
    h_start = h_function(start)
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
        for neighbour in get_neighbours(current):
            g_new = g[current] + 1
            if (neighbour not in g) or (g_new < g[neighbour]):
                parents[neighbour] = current
                g[neighbour] = g_new

                h_neighbour = h_function(neighbour)
                f_neighbour = g[neighbour] + h_neighbour
                heapq.heappush(queue, (f_neighbour, h_neighbour, neighbour))

    path, length = get_path_from_parents(start, goal, parents)
    return (path, length, expanded)


def main():

    print(f"goal:{goal}")
    print(f"state:{state}")

    # Run the A* Search
    path_astar, length_astar, expanded_astar = astar_search(h_function=md)
    print(f"\nA* Search:\tlength: {length_astar}, expanded: {len(expanded_astar)}")


if __name__ == "__main__":
    main()