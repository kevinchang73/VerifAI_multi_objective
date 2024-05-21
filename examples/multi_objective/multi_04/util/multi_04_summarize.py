import sys
from collections import Counter
dir_name = sys.argv[1]

# Segment 0
#print("Segment 0")
file_names = ['result_multi_04_demab0.txt', 'result_multi_04_dmab0.txt', 'result_multi_04_dce0.txt', 'result_multi_04_halton.txt', 'result_multi_04_random.txt', 'result_multi_04_single.txt', 'result_multi_04_udemab.txt']

# Segment 1
print("Segment 1")
file_names = ['result_multi_04_demab1.txt', 'result_multi_04_dmab1.txt', 'result_multi_04_random.txt', 'result_multi_04_single.txt']
for file in file_names:
    print(f"File: {file}")
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    line = lines[4].split('[')[1].split(']')[0].split(',')
    line = [int(num) for num in line]
    counts = Counter(line)
    sorted_counts = sorted(counts.items(), key=lambda x: x[0], reverse=True)
    for number, count in sorted_counts:
        print(f"Number {number} appears {count} times.")
    print()

# Segment 2
#print("Segment 2")
file_names = ['result_multi_04_demab2.txt', 'result_multi_04_dmab2.txt', 'result_multi_04_dce2.txt', 'result_multi_04_halton.txt', 'result_multi_04_random.txt', 'result_multi_04_single.txt', 'result_multi_04_udemab.txt']
