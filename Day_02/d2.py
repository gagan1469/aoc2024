from math import copysign

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

# safe report rules
# all increasing or all decreasing
# difference is at least 1 and at most 3
def is_safe(report: list, control: set = set([1, 2, 3])):
    safe = False
    levels = [int(i) for i in report]
    deltas = set([abs(levels[i+1] - levels[i]) for i in range(0, len(levels)-1)])
    signs = set([copysign(1, levels[i+1] - levels[i]) for i in range(0, len(levels)-1)])

    if len(signs) == 1 and len(deltas - control) == 0:
        safe = True
    # else:
    # # unsafe due to sign changes
    #     if len(signs) > 1:
    #         print(f'Unsafe report detected due to sign change.\t{levels}\t{signs}')
    #     elif len(deltas - control) > 0:
    #         print(f'Unsafe report detected due low/high change.\t{levels}\t{deltas - control}')

    return safe

def main():
    fname = 'Day_02\inputs.txt'
    # fname = 'Day_02\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    # print(lines)

    safe_reports = 0
    unsafe_reports = []

    for line in lines: 
        report = line.split()       
        safe = is_safe(report)

        if safe == True:
            safe_reports += 1
        else:
            unsafe_reports.append(report)

    print()
    print('Part A answer:')
    print(f'Safe reports {safe_reports}')
    print(f'Unsafe reports {len(unsafe_reports)}')
    print()

    # part B requires 1 violation to be forgiven
    # each report has different number of levels (5 to 8)
    # process only unsafe reports
    # Try a brute force method.
    # drop a level from each sequence
    # check if that makes it safe
    # report could be made safe by more than 1 single change but do not double count the ways in which the report can be made safe!
    new_safe_reports = 0
    
    for report_num, report in enumerate(unsafe_reports):
        for i in range(len(report)):
            trial = [report[j] for j in range(len(report)) if j != i]
            safe = is_safe(trial)

            if safe == True:
                print(f'ALERT:::Safe report detected.\t{report_num}\t{i}\t{report}\t{trial}')
                new_safe_reports += 1
                break

    print()        
    print('Part B answer:')
    print(f'Original safe reports {safe_reports}')
    print(f'Additional safe reports {new_safe_reports}')
    print(f'Total safe reports {safe_reports + new_safe_reports}')

    # For part A answer was accepted. 564
    # For part B, the first pass gave 54 additional for a total of 618. That was not accepted!
    # because some combinations were being double counted.
    # Redo by generating trials and testing each permutation.
    # This gave 40 additional safe reports. Final answer 604.


if __name__ == '__main__':
    main()