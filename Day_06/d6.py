# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    # print(lines)
    # convert to matrix

    m = [''] * len(lines)
    for i, line in enumerate(lines):
        n = [''] * len(line)
        for j, c in enumerate(line):
            n[j] = c
        m[i] = n

    size = [len(m), len(n)]    
    # print(m)
    return m, size

def locate_guard(grid: list, directions: list):
    current_location = [-1, -1]
    facing_direction = ''
    
    for i in range(0, len(grid)):
        section = grid[i]
        for dir in directions:
            if dir in section:
                j = section.index(dir)
                current_location = [i, j]
                facing_direction = dir
                break

    return current_location, facing_direction

def check_obstruction(proposed_position: list, grid: list, obstructions: list = ['#', 'O']):
    obstructed = False
    grid_size = [len(grid), len(grid[0])]
    off_grid = check_off_grid(proposed_position, grid_size)

    if not off_grid and grid[proposed_position[0]][proposed_position[1]] in obstructions:
        obstructed = True

    return obstructed, off_grid

def check_guard_in_loop(new_locations_visited: int, moves_made: int, moves_threshold: int = 100):
    guard_in_loop = False

    if new_locations_visited == 0 and moves_made > moves_threshold:
        guard_in_loop = True

    return guard_in_loop

def navigate_grid(grid: list, directions: list):
    guard_in_loop = False
    guard_loc, guard_dir = locate_guard(grid, directions)
    grid_size = [len(grid), len(grid[0])]
    off_grid = check_off_grid(guard_loc, grid_size)
    # print(guard_loc, guard_dir, off_grid)

    prev_visited_count = 0
    counter = 0
    while not off_grid and not guard_in_loop:
        # off_grid = check_off_grid(guard_loc, grid_size)
        mark_visited(guard_loc, grid)
        visited_count = count_visited(grid)
        visited_count_change = visited_count - prev_visited_count
        
        if visited_count_change == 0:
            counter += 1

        # stuck in loop test
        # if no new locations have been visited in 1 x already visited locations (= one full circuit), 
        guard_in_loop = check_guard_in_loop(visited_count_change, counter, int(1*visited_count))
        prev_visited_count = visited_count
        guard_loc, guard_dir, off_grid = move_guard(guard_loc, guard_dir, grid, directions)

        # print(guard_loc, guard_dir, off_grid, guard_in_loop, visited_count_change, counter)
    return visited_count, off_grid, guard_in_loop

def place_new_obstruction(proposed_position: list, grid: list, new_obstruction: str = 'O'):
    grid[proposed_position[0]][proposed_position[1]] = new_obstruction    
    return grid

def get_obstruction_candidates(guard_origin: list, visited_grid: list, visit_marker: str = 'X'):
    obstruction_candidates = []

    # clear guard origin as a candidate
    visited_grid[guard_origin[0]][guard_origin[1]] = ''

    for i, row in enumerate(visited_grid):
        for j, c in enumerate(row):
            if c == visit_marker:
                obstruction_candidates.append([i, j])

    return obstruction_candidates
    
def mark_visited(current_position: list, grid: list, marker: str = 'X'):
    grid[current_position[0]][current_position[1]] = marker
    return

def count_visited(grid: list, marker: str = 'X'):
    total_visited = 0
    for row in grid:
        total_visited += row.count(marker)

    return total_visited

def check_off_grid(current_position: list, grid_size: list):
    off_grid = False
    if current_position[0] < 0 or current_position[0] >= grid_size[0] \
        or current_position[1] < 0 or current_position[1] >= grid_size[1]:
        off_grid = True

    return off_grid

def move_guard(current_position: list, current_direction: str, grid: list, directions: list):
    delta_row = 0
    delta_col = 0
    next_direction = current_direction
    if current_direction == '^':
        delta_row = -1
        next_direction = '>'
    elif current_direction == '>':
        delta_col = +1
        next_direction = 'V'
    elif current_direction == 'V':
        delta_row = +1
        next_direction = '<'
    else:
        delta_col = -1
        next_direction = '^'

    next_position = [current_position[0] + delta_row, current_position[1] + delta_col] 
    path_blocked, off_grid = check_obstruction(next_position, grid)
    
    if path_blocked == True:
        next_position, next_direction, off_grid = move_guard(current_position, next_direction, grid, directions)
    else:
        next_direction = current_direction

    return next_position, next_direction, off_grid

def main():
    fname = 'Day_06\inputs.txt'
    # fname = 'Day_06\sample_inputs.txt'

    directions = ['>', '<', '^', 'V']
    grid, _ = load_data_set(data_file=fname)

    guard_origin, _ = locate_guard(grid, directions)
    visited_count, _, _ = navigate_grid(grid, directions)
    print(f'Part A answer: {visited_count}')
    
    #for line in grid:
    #    print(line)

    # Part B
    # place new obstruction. obstruction location candidates are locations the guard has 
    # visited except the guard origin location.
    # move guard detect looping
    obstruction_candidates = get_obstruction_candidates(guard_origin, grid)
    loop_locations = []
    for i, candidate in enumerate(obstruction_candidates):
        # print(f'Testing obstruction at location {candidate}')
        # reload the grid
        trial_grid, _ = load_data_set(data_file=fname)
        trial_grid = place_new_obstruction(candidate, trial_grid)
        _, _, guard_in_loop = navigate_grid(trial_grid, directions)

        if guard_in_loop:
            loop_locations.append(candidate)
            print(f'Total tested {i}, candidates found {len(loop_locations)}, Loop location for new obstruction at {candidate}')

    print(f'Part B answer: {len(loop_locations)}')

if __name__ == '__main__':
    main()