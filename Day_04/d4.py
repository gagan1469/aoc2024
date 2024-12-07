import re

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def transpose_data(data: str):
    orig_rows = len(data)
    orig_columns = 0

    for dt in data:
        if len(dt) > orig_columns:
            orig_columns = len(dt)
            print(f'Column length in matrix updated to {orig_columns}')


    transpose = [''] * orig_columns
    for dt in data:
        for i, c in enumerate(dt):
            transpose[i] += c

    return transpose

def diagonal_data(data: str):
    all_diagonals = []
    diagonals = [''] * len(data[0])
    
    # forward upper diagonals
    for i, dt in enumerate(data):
        idx = 0
        for j in range(i, len(dt)):
            diagonals[idx] += dt[j]
            idx += 1

    for d in diagonals:
        all_diagonals.append(d)

    # reverse upper diagonals
    diagonals = [''] * len(data[0])
    for i, dt in enumerate(data):
        idx = 0
        for j in range(len(dt)-i, 0, -1):
            diagonals[idx] += dt[j-1]
            idx += 1

    for d in diagonals:
        all_diagonals.append(d)

    # forward lower diagonals
    diagonals = [''] * len(data[0])
    for i, dt in enumerate(data):
        idx = 0
        for j in range(i, 0, -1):
            diagonals[idx] += dt[j-1]
            #print(i, j , idx, dt[j-1])
            idx += 1

    for d in diagonals:
        all_diagonals.append(d)

    # reverse lower diagonals
    diagonals = [''] * len(data[0])
    for i, dt in enumerate(data):
        idx = 0
        for j in range(len(dt)-i, len(dt), 1):
            diagonals[idx] += dt[j]
            # print(i, j , idx, dt[j], dt)
            idx += 1

    # print(diagonals)
    for d in diagonals:
        all_diagonals.append(d)

    return all_diagonals

def extract_main_expression(input: str, find_expression: str):
    pattern = re.compile(find_expression)
    result = pattern.findall(input)
    return result

def main():
    fname = 'Day_04\inputs.txt'
    # fname = 'Day_04\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    # print(lines)

    expr1 = 'XMAS'
    expr2 = 'SAMX'
    total = 0
    # simple horizontal find
    for line in lines:
        result = extract_main_expression(line, expr1)
        # print(f'Found horizontal fwd {len(result)}')
        total += len(result)
        result = extract_main_expression(line, expr2)
        # print(f'Found horizontal bwd {len(result)}')
        total += len(result)

    print(f'Total found in horizontals: {total}')

    # transpose and find in vertical
    transposed = transpose_data(lines)
    # print(transposed)

    for line in transposed:
        result = extract_main_expression(line, expr1)
        # print(f'Found vertical fwd {len(result)}')
        total += len(result)
        result = extract_main_expression(line, expr2)
        # print(f'Found vertical bwd {len(result)}')
        total += len(result)

    print(f'Total found h+v: {total}')

    # find in diagonals
    diagonal = diagonal_data(lines)
    # print(diagonal)

    for line in diagonal:
        result = extract_main_expression(line, expr1)
        # print(f'Found horizontal fwd {len(result)}')
        total += len(result)
        result = extract_main_expression(line, expr2)
        # print(f'Found horizontal bwd {len(result)}')
        total += len(result)

    print(f'Total found h+v+d: {total}')

if __name__ == '__main__':
    main()