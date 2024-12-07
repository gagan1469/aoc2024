# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    test_values = []
    input_values = []

    for line in lines:
        temp = line.split(':')
        test_values.append(int(temp[0]))
        temp2 = temp[1].split()
        vals = []
        for t in temp2:
            vals.append(int(t))
        input_values.append(vals)

    return test_values, input_values

def calculate_pair(a: int, b: int, operator: str):
    result = 0
    if operator == '+':
        result = a + b
    elif operator == '*':
        result = a * b
    elif operator == '||':
        temp = str(a) + str(b)
        result = int(temp)
    
    return result

def calculate_permutation(input_values: list, operations: list):
    #initialize
    result = input_values[0]
    for i in range(1, len(input_values)):
        result = calculate_pair(result, input_values[i], operations[i-1])
    return result

def add_permutation_level(permutations: list, current_level_options: list):
    # is existing permuations is p, and options for next level is q, new permutations will be pq
    new_permutations = []
    for option in current_level_options:
        for permutation in permutations:
            new_permutation = [p for p in permutation]
            new_permutation.append(option)
            new_permutations.append(new_permutation)
    
    return new_permutations

def get_permutations(operator_locations: int, operators: list = ['+', '*']):
    # seed the first level permutations
    permutations = [''] * len(operators)        
    for i in range(len(operators)):
        permutations[i] = [operators[i]]

    # handle subsequent level of permutations
    for i in range(1, operator_locations):    
        permutations = add_permutation_level(permutations, operators)
    
    return permutations

def match_test_value(test_value: int, input_values: list, operators: list = ['+', '*']):
    operator_locations = len(input_values) -1
    permutations = get_permutations(operator_locations, operators)
    match_found = False

    for permutation in permutations:
        calc_value = calculate_permutation(input_values, permutation)
        if calc_value == test_value:
            match_found = True
            break

    return match_found, permutation

def main():
    fname = 'Day_07\inputs.txt'
    # fname = 'Day_07\sample_inputs.txt'

    test_values, input_values = load_data_set(data_file=fname)

    valid_sum = 0
    for tv, iv in zip(test_values, input_values):
        matched, _ = match_test_value(tv, iv)
        # print(tv, iv, matched)
        if matched:
            valid_sum += tv

    print(f'Part A answer: {valid_sum}')

    # part B:
    operators = ['+', '*', '||']
    valid_sum = 0
    for tv, iv in zip(test_values, input_values):
        matched, _ = match_test_value(tv, iv, operators)
        # print(tv, iv, matched)
        if matched:
            valid_sum += tv

    print(f'Part B answer: {valid_sum}')
if __name__ == '__main__':
    main()