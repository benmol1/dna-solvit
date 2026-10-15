
import random

goal  = (0,1,2,3,4,5,6,7,8)
state = (1,2,3,0,4,5,6,7,8)  

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

    for jj in range(1000):
        random_state = random_solvable_state()
        md_value = md(random_state)
        mp_value = misplaced_tiles(random_state)
        assert md_value >= mp_value, f"{random_state}: md={md_value}, mp={mp_value}"

    print("MD >= MP held for all 1000 random solvable states")


print(f"goal:{goal}")
print(f"state:{state}")

print(f"Total MD excluding blank tile: {md(state, False)}")
print(f"Total MP excluding blank tile: {misplaced_tiles(state, False)}")

assert_md_dominates_mp()