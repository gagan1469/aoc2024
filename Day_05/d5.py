# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    page_ordering_rules = []
    printing_instructions = []
    rule_delimiter = '|'
    instruction_delimiter = ','
    for line in lines:
        if len(line) > 0:
            if rule_delimiter in line:
                rule = line.split(rule_delimiter)
                page_ordering_rules.append(rule)
            elif instruction_delimiter in line:
                instruction = line.split(instruction_delimiter)
                printing_instructions.append(instruction)
    
    return printing_instructions, page_ordering_rules

def get_dependencies(page: str, rules: list):
    predecessors = []
    successors = []
    for rule in rules:
        if page in rule:
            if page in rule[0]:
                successors.append(rule[1])
            else:
                predecessors.append(rule[0])

    return predecessors, successors

def validate_instruction(instruction: list, rules: list):
    valid = True

    for i, page in enumerate(instruction):
        predecessors, successors = get_dependencies(page, rules)
        # print(page, predecessors, successors)

        # predecessors are in succeeding sequence, instruction is invalid
        for j in range(i+1, len(instruction)):
            if instruction[j] in predecessors:
                valid = False
                break

        # is successors are in preceding sequence, instruction is invalid
        for j in range(0, i):
            if instruction[j] in successors:
                valid = False
                break

    return valid

def get_middle_number(input: list):
    count = len(input)
    middle_value: int

    if count % 2 == 1:
        # odd vallue
        middle_value = input[int(count/2)]
        # print(middle_value)
    else:
        print('even:::')
        middle_value = (input[count/2] + input[count/2 + 1]) / 2
    
    return middle_value

# take a bad instruction and reorder it until fixed
def fix_instruction(instruction: list, rules: list):
    valid = False
    new_instruction = [i for i in instruction]
    while valid == False:
        recheck = False
        for i, page in enumerate(instruction):
            predecessors, successors = get_dependencies(page, rules)

            # a predecessor is in succeeding sequence, swap and start over
            for j in range(i+1, len(instruction)):
                # print(instruction[i], instruction[j])
                if instruction[j] in predecessors:
                    temp = new_instruction[i]
                    new_instruction[i] = new_instruction[j]
                    new_instruction[j] = temp
                    recheck = True
                    break

            # a successors is in preceding sequence, swap and start over
            if recheck == False:
                for j in range(0, i):
                    if instruction[j] in successors:
                        temp = new_instruction[i]
                        new_instruction[i] = new_instruction[j]
                        new_instruction[j] = temp
                        recheck = True
                        break

            valid = validate_instruction(new_instruction, rules)
            # print(new_instruction)
            instruction = new_instruction

    return new_instruction

def main():
    fname = 'Day_05\inputs.txt'
    # fname = 'Day_05\sample_inputs.txt'

    instructions, rules = load_data_set(data_file=fname)
    # print(instructions)
    # print(rules)
    total = 0
    total_b = 0
    for instuction in instructions:
        valid = validate_instruction(instuction, rules)
        # print(valid, instuction)
        if valid == True:
            mid = get_middle_number(instuction)
            total += int(mid)
        else:
            # fix instruction
            new_instruction = fix_instruction(instuction, rules)
            mid_b = get_middle_number(new_instruction)
            total_b += int(mid_b)

    print(f'Part A answer: {total}')
    print(f'Part B answer: {total_b}')    

if __name__ == '__main__':
    main()