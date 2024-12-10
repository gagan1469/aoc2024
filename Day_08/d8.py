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

def get_location_key(grid: list, empty_location: str = '.'):
    location_key = dict()
    
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != empty_location:
                if c in location_key:
                    # add location
                    location_key[c].append([i,j])
                else:
                    # add key and location
                    location_key[c] = [[i,j]]

    return location_key

def check_off_grid(location: list, grid_size: list):
    off_grid = False

    if location[0] < 0 or location[1] < 0 or \
        location[0] >= grid_size[0] or \
        location[1] >= grid_size[1]:
        off_grid = True
    
    return off_grid

def get_antinodes(location1: list, location2: list, grid_size: list):
    antinode1 = None
    antinode2 = None
    delta_row = location1[0] - location2[0]
    delta_col = location1[1] - location2[1]

    temp_node = [location1[0] + delta_row, location1[1] + delta_col]
    off_grid = check_off_grid(temp_node, grid_size)
    if not off_grid:
        antinode1 = temp_node

    temp_node = [location2[0] - delta_row, location2[1] - delta_col]
    off_grid = check_off_grid(temp_node, grid_size)
    if not off_grid:
        antinode2 = temp_node

    return antinode1, antinode2

def get_resonant_harmonics_antinodes(location1: list, location2: list, grid_size: list):
    antinodes = []
    delta_row = location1[0] - location2[0]
    delta_col = location1[1] - location2[1]

    off_grid = False
    temp_node = [location1[0], location1[1]]
    while not off_grid:
        temp_node = [temp_node[0] + delta_row, temp_node[1] + delta_col]
        off_grid = check_off_grid(temp_node, grid_size)
        if not off_grid:
            antinodes.append(temp_node)

    off_grid = False
    temp_node = [location2[0], location2[1]]
    while not off_grid:
        temp_node = [temp_node[0] - delta_row, temp_node[1] - delta_col]
        off_grid = check_off_grid(temp_node, grid_size)
        if not off_grid:
            antinodes.append(temp_node)

    return antinodes

def process_antennae(locations: list, grid_size: list):
    antinodes = []
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            antinode1, antinode2 = get_antinodes(locations[i], locations[j], grid_size)
            if antinode1 is not None:
                antinodes.append(antinode1)
            if antinode2 is not None:
                antinodes.append(antinode2)
    
    return antinodes

def process_resonant_harmonics_antennae(locations: list, grid_size: list):
    all_antinodes = []
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            antinodes = get_resonant_harmonics_antinodes(locations[i], locations[j], grid_size)
            for antinode in antinodes:
                all_antinodes.append(antinode)
    return all_antinodes

def plot_antinodes(antinode_locations: list, grid: list, empty_location: str = '.', antinode_marker: str = '#'):
    for location in antinode_locations:
        loc_marker = grid[location[0]][location[1]]
        grid[location[0]][location[1]] = antinode_marker
        if loc_marker == empty_location:
            grid[location[0]][location[1]] = antinode_marker

    return
    
def main():
    fname = 'Day_08\inputs.txt'
    #fname = 'Day_08\sample_inputs.txt'

    m, size = load_data_set(data_file=fname)
    print(size)
    
    # for i in m:
    #     print(i)

    tower_location_freq = get_location_key(m)

    print(tower_location_freq)
    
    all_antinodes = []
    for k in tower_location_freq.keys():
        locations = tower_location_freq[k]
        antinodes = process_antennae(locations, size)
        for node in antinodes:
            if node not in all_antinodes:
                all_antinodes.append(node)
        # print(antinodes)

    # print(all_antinodes, len(all_antinodes))
    # plot_antinodes(all_antinodes, m)
    # for i in m:
    #     print(i)

    print(f'Part A answer: {len(all_antinodes)}')

    all_antinodes = []
    for k in tower_location_freq.keys():
        locations = tower_location_freq[k]
        antinodes = process_resonant_harmonics_antennae(locations, size)
        for node in antinodes:
            if node not in all_antinodes:
                all_antinodes.append(node)

        # plus all tower locations are antinodes
        for location in locations:
            if location not in all_antinodes:
                all_antinodes.append(location)
    
    # print(all_antinodes, len(all_antinodes))
    print(f'Part B answer: {len(all_antinodes)}')

    # for i in m:
    #     print(i)

    # print()
    # plot_antinodes(all_antinodes, m)
    # for i in m:
    #     print(i)

if __name__ == '__main__':
    main()