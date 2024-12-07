# read the inputs
# lines = open("sample_inputs.txt").read().split("\n")
lines = open("Day_01\inputs.txt").read().split("\n")
# print(lines)

# Part A
list_1 = []
list_2 = []

for line in lines:
    v1, v2 = line.split()
    list_1.append(int(v1))
    list_2.append(int(v2))

list_1 = sorted(list_1)
list_2 = sorted(list_2)

diff = 0

for v1, v2 in zip(list_1, list_2):
    diff += abs(v1-v2)

print('Part A answer:')
print(diff)

# Part B
# list_1 > find element count in list 2

found_count = 0
sim_index = 0
for v1 in list_1:
    if v1 in list_2:
        found_count += 1
        k = list_2.count(v1)
        sim_index += k * v1

print('Part B answer:')
print(sim_index)
print(f'Matching values in list_2: {found_count}')

