import re
# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    print(lines)
    # convert to matrix
    m = [''] * len(lines)
    for i, line in enumerate(lines):
        n = [''] * len(line)
        for j, c in enumerate(line):
            # print(i, j, c)
            n[j] = c
        m[i] = n
        
    print(m)
    return m

def process_data(data: list):
    match = 'A'
    expr = ['MAS', 'SAM']

    candidate = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data)-1):
            if data[i][j] == match:
                #candidate
                diag1 = data[i-1][j-1] + data[i][j] + data[i+1][j+1]
                diag2 = data[i-1][j+1] + data[i][j] + data[i+1][j-1]
                if diag1 in expr and diag2 in expr:
                    candidate += 1
                    print(i, j, candidate, diag1, diag2)
                    
    return candidate

def main():
    fname = 'Day_04\inputs.txt'
    # fname = 'Day_04\sample_inputs.txt'

    matrix_in = load_data_set(data_file=fname)
    # print(lines)

    total = 0
    total = process_data(matrix_in)

    print(f'Total found: {total}')

if __name__ == '__main__':
    main()