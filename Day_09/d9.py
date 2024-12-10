# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    line = lines[0]
    file_blocks_counts = [int(line[i]) for i in range(0, len(line), 2)]
    empty_blocks_counts = [int(line[i]) for i in range(1, len(line), 2)]

    return file_blocks_counts, empty_blocks_counts

def expand_single_block_pair(file_number: str, file_blocks_count: int, empty_blocks_count: int = 0, empty_marker: str = '.'):
    file_map = [file_number] * file_blocks_count
    empty_map = [empty_marker] * empty_blocks_count 
    file_map.extend(empty_map)

    return file_map
    
def build_expanded_notation(file_blocks_counts: list, empty_blocks_counts: list):
    exanded_disk_map = []

    for file_num, (file_blocks, empty_blocks) in enumerate(zip(file_blocks_counts, empty_blocks_counts)):
        file_map = expand_single_block_pair(str(file_num), file_blocks, empty_blocks)
        # print(file_num, file_blocks, empty_blocks, file_map)
        exanded_disk_map.extend(file_map)

    # all pairs have been processed, handle the last file with no empty spaces at the end
    file_blocks = file_blocks_counts[-1]
    file_num = len(file_blocks_counts) - 1
    file_map = expand_single_block_pair(str(file_num), file_blocks)
    exanded_disk_map.extend(file_map)

    return exanded_disk_map
    
def swap_blocks(disk_map: list, empty_location: int, file_block_location: int):
    swapped = 0
    if empty_location < file_block_location:
        temp = disk_map[empty_location]
        disk_map[empty_location] = disk_map[file_block_location]
        disk_map[file_block_location] = temp
        swapped = 1

    return swapped

def get_last_file_block(disk_map: list, search_location: int = -1, empty_marker: str = '.'):
    last_file_block = disk_map[search_location]
    
    while last_file_block == empty_marker:
        search_location -= 1
        last_file_block = disk_map[search_location]

    return last_file_block, search_location

def get_first_empty_block(disk_map: list, search_location: int = 0, empty_marker: str = '.'):
    first_empty_block_loc = disk_map.index(empty_marker, search_location)

    return first_empty_block_loc

def consolidate_empty_blocks(disk_map: list, empty_marker: str = '.'):
    total_swaps = 0
    last_file_block_loc = len(disk_map) - 1
    _ , last_file_block_loc = get_last_file_block(disk_map, last_file_block_loc)
    first_empty_block_loc = get_first_empty_block(disk_map)

    while last_file_block_loc > first_empty_block_loc:
        total_swaps += swap_blocks(disk_map, first_empty_block_loc, last_file_block_loc)
        _ , last_file_block_loc = get_last_file_block(disk_map, last_file_block_loc)
        first_empty_block_loc = get_first_empty_block(disk_map)
        # print(total_swaps, disk_map)

    return

def get_file_location(disk_map: list, block_id: int):
    # num_blocks = blocks[block_id]
    start_pos = disk_map.index(str(block_id), 0)
    return start_pos #, num_blocks


def get_empty_location(disk_map: list, slot_id: int,  search_start: int = 0, empty_marker: str = '.'):
    try:
        search_start = get_file_location(disk_map, slot_id)
        start_pos = disk_map.index(empty_marker, search_start)
    except ValueError as e:
        start_pos = -1

    return start_pos

def rearrange_file(disk_map: list, file_id: int, file_size: int, available_slots: list):
    rearranged = False

    for i, slot_size in enumerate(available_slots):
        
        if file_size <= slot_size and file_id > i:
            slot_start_pos = get_empty_location(disk_map, i)
            file_start_pos = get_file_location(disk_map, file_id)

            for j in range(0, file_size):
                disk_map[slot_start_pos + j] = str(file_id)
                disk_map[file_start_pos + j] = '.'

            rearranged = True
            available_slots[i] -= file_size
            available_slots[file_id-1] += file_size        
        
        if rearranged == True:
            break

    return rearranged

def consolidate_files(disk_map: list, files: list, available_slots: list):
    for i in range(len(files)-1, 0, -1):
        file_id = i
        file_size = files[i]
        rearranged = rearrange_file(disk_map, file_id, file_size, available_slots)
        # print(file_id, file_size, available_slots, rearranged)
        # print(disk_map)

def calcuate_checksum(disk_map: list, empty_marker: str = '.'):
    checksum = 0
    for i, file_id in enumerate(disk_map):
        if file_id != empty_marker:
            checksum += i * int(file_id)

    return checksum

def main():
    fname = 'Day_09\inputs.txt'
    # fname = 'Day_09\sample_inputs.txt'

    file_blocks_counts, empty_blocks_counts = load_data_set(data_file=fname)
    
    print('processing...')
    print(len(file_blocks_counts), len(empty_blocks_counts))

    full_disk_map = build_expanded_notation(file_blocks_counts, empty_blocks_counts)

    consolidate_empty_blocks(full_disk_map)
    checksum = calcuate_checksum(full_disk_map)
    print(f'Part A answer: {checksum}')

    # part B
    # reload
    full_disk_map = build_expanded_notation(file_blocks_counts, empty_blocks_counts)
    consolidate_files(full_disk_map, file_blocks_counts, empty_blocks_counts)
    checksum = calcuate_checksum(full_disk_map)
    print(f'Part B answer: {checksum}')

if __name__ == '__main__':
    main()