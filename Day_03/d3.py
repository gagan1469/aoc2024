import re

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def extract_main_expression(input: str, find_expression: str):
    pattern = re.compile(find_expression)
    result = pattern.findall(input)
    return result

def calculate_product(input: str, find_expression: str):
    pattern = re.compile(find_expression)
    vals = pattern.findall(input)
    product = int(vals[0]) * int(vals[1])
    return product

def calculate(input: str, find_expression: str):
    target = '[0-9]{1,3}'
    enabled = True
    answer = 0

    for line in input:
        result = extract_main_expression(line, find_expression=find_expression)

        print(f'Parsed pairs: {len(result)}')
        for r in result:
            print(f'Found: {r}')

            if r == 'do':
                enabled = True
            elif r == 'don\'t':
                enabled = False
            else:
                if enabled:
                    product = calculate_product(r, target)
                    answer += product

    return answer

def main():
    fname = 'Day_03\inputs.txt'
    # fname = 'Day_03\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    print(f'Input size: {len(lines)}')

    # Part A 
    find_expression_a = 'mul\({1}[0-9]{1,3},[0-9]{1,3}\){1}'
    ans_a = calculate(lines, find_expression_a
                      )
    # Part B regex
    find_expression_b = 'don\'t|do|mul\({1}[0-9]{1,3},[0-9]{1,3}\){1}'
    ans_b = calculate(lines, find_expression_b)

    print()
    print('Part A answer:')
    print(f'Uncorrupted stock {ans_a}')
    print()
    print('Part B answer:')
    print(f'Uncorrupted stock with additional instructions {ans_b}')


if __name__ == '__main__':
    main()

""" 
Results
Part A answer:
Uncorrupted stock 161085926

Part B answer:
Uncorrupted stock with additional instructions 82045421
""" 
