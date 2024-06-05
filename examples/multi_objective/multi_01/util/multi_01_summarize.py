import sys
dir_name = sys.argv[1]

# Segment 0
'''
print("Segment 0")
file_names = ['result_multi_01_demab0.txt', 'result_multi_01_dmab0.txt', 'result_multi_01_dce0.txt', 'result_multi_01_halton.txt', 'result_multi_01_random.txt', 'result_multi_01_single.txt', 'result_multi_01_udemab.txt']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    to_print = []
    ce_types = {}
    ce_section = False
    target_segment = False

    for i in range(len(lines)):
        line = lines[i].strip()
        
        if i == 2:
            parts = line.split()
            to_print.append(float(parts[3]) / 2.0)
            to_print.append(float(parts[1]) / 2.0)
            to_print.append(float(parts[5]))
        elif line.startswith("Counterexample"):
            ce_section = True
        elif ce_section and line.startswith("segment 0"):
            target_segment = True
        elif target_segment:
            if line.startswith("Types"):
                to_print.append(int(line.split()[1]))
            elif line.startswith("("):
                type_info = line.split(':')
                type_key = type_info[0].strip()
                type_count = int(type_info[1].strip())
                ce_types[type_key] = type_count
            else:
                if "(0, 0)" in ce_types:
                    to_print.append(ce_types["(0, 0)"])
                else:
                    to_print.append(0)
                if "(0, 1)" in ce_types:
                    to_print.append(ce_types["(0, 1)"])
                else:
                    to_print.append(0)
                if "(1, 0)" in ce_types:
                    to_print.append(ce_types["(1, 0)"])
                else:
                    to_print.append(0)
                if "(1, 1)" in ce_types:
                    to_print.append(ce_types["(1, 1)"])
                else:
                    to_print.append(0)      
                target_segment = False
                ce_section = False
        elif line.startswith("Standard deviation of"):
            parts = line.split()
            to_print.append(float(parts[4]))

    for item in to_print:
        print(round(item, 4), end=' ')
    print()

# Segment 1
print("Segment 1")
file_names = ['result_multi_01_demab1.txt', 'result_multi_01_dmab1.txt', 'result_multi_01_dce1.txt', 'result_multi_01_halton.txt', 'result_multi_01_random.txt', 'result_multi_01_single.txt', 'result_multi_01_udemab.txt']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    to_print = []
    ce_types = {}
    ce_section = False
    target_segment = False

    for i in range(len(lines)):
        line = lines[i].strip()
        
        if i == 4:
            parts = line.split()
            to_print.append(float(parts[3]) / 3.0)
            to_print.append(float(parts[1]) / 3.0)
            to_print.append(float(parts[5]))
        elif line.startswith("Counterexample"):
            ce_section = True
        elif ce_section and line.startswith("segment 1"):
            target_segment = True
        elif target_segment:
            if line.startswith("Types"):
                to_print.append(int(line.split()[1]))
            elif line.startswith("("):
                type_info = line.split(':')
                type_key = type_info[0].strip()
                type_count = int(type_info[1].strip())
                ce_types[type_key] = type_count
            else:
                if "(0, 0)" in ce_types:
                    to_print.append(ce_types["(0, 0)"])
                else:
                    to_print.append(0)
                if "(0, 1)" in ce_types:
                    to_print.append(ce_types["(0, 1)"])
                else:
                    to_print.append(0)
                if "(1, 0)" in ce_types:
                    to_print.append(ce_types["(1, 0)"])
                else:
                    to_print.append(0)
                if "(1, 1)" in ce_types:
                    to_print.append(ce_types["(1, 1)"])
                else:
                    to_print.append(0)      
                target_segment = False
                ce_section = False
        elif line.startswith("Standard deviation of"):
            parts = line.split()
            to_print.append(float(parts[4]))

    for item in to_print:
        print(round(item, 4), end=' ')
    print()
'''

print("Exploration ratio")
file_names = ['result_multi_01_demab1_1.txt', 'result_multi_01_demab1.txt', 'result_multi_01_demab1_2.txt', 'result_multi_01_demab1_3.txt', 'result_multi_01_demab1_4.txt']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    to_print = []
    ce_types = {}
    ce_section = False
    target_segment = False

    for i in range(len(lines)):
        line = lines[i].strip()
        
        if i == 4:
            parts = line.split()
            to_print.append(float(parts[3]) / 3.0)
            to_print.append(float(parts[1]) / 3.0)
            to_print.append(float(parts[5]))
        elif line.startswith("Counterexample"):
            ce_section = True
        elif ce_section and line.startswith("segment 1"):
            target_segment = True
        elif target_segment:
            if line.startswith("Types"):
                to_print.append(int(line.split()[1]))
            elif line.startswith("("):
                type_info = line.split(':')
                type_key = type_info[0].strip()
                type_count = int(type_info[1].strip())
                ce_types[type_key] = type_count
            else:
                if "(0, 0)" in ce_types:
                    to_print.append(ce_types["(0, 0)"])
                else:
                    to_print.append(0)
                if "(0, 1)" in ce_types:
                    to_print.append(ce_types["(0, 1)"])
                else:
                    to_print.append(0)
                if "(1, 0)" in ce_types:
                    to_print.append(ce_types["(1, 0)"])
                else:
                    to_print.append(0)
                if "(1, 1)" in ce_types:
                    to_print.append(ce_types["(1, 1)"])
                else:
                    to_print.append(0)      
                target_segment = False
                ce_section = False
        elif line.startswith("Standard deviation of"):
            parts = line.split()
            to_print.append(float(parts[4]))

    for item in to_print:
        print(round(item, 4), end=' ')
    print()

'''
# Segment 2
print("Segment 2")
file_names = ['result_multi_01_demab2.txt', 'result_multi_01_dmab2.txt', 'result_multi_01_dce2.txt', 'result_multi_01_halton.txt', 'result_multi_01_random.txt', 'result_multi_01_single.txt', 'result_multi_01_udemab.txt']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    to_print = []
    ce_types = {}
    ce_section = False
    target_segment = False

    for i in range(len(lines)):
        line = lines[i].strip()
        
        if i == 6:
            parts = line.split()
            to_print.append(float(parts[3]) / 1.0)
            to_print.append(float(parts[1]) / 1.0)
            to_print.append(float(parts[5]))
        elif line.startswith("Counterexample"):
            ce_section = True
        elif ce_section and line.startswith("segment 2"):
            target_segment = True
        elif target_segment:
            if line.startswith("Types"):
                to_print.append(int(line.split()[1]))
            elif line.startswith("("):
                type_info = line.split(':')
                type_key = type_info[0].strip()
                type_count = int(type_info[1].strip())
                ce_types[type_key] = type_count
            else:
                if "(0,)" in ce_types:
                    to_print.append(ce_types["(0,)"])
                else:
                    to_print.append(0)
                to_print.append(0) # (0,1)
                if "(1,)" in ce_types:
                    to_print.append(ce_types["(1,)"])
                else:
                    to_print.append(0)
                to_print.append(0) # (1,1)  
                target_segment = False
                ce_section = False
        elif line.startswith("Standard deviation of"):
            parts = line.split()
            to_print.append(float(parts[4]))

    for item in to_print:
        print(round(item, 4), end=' ')
    print()
'''