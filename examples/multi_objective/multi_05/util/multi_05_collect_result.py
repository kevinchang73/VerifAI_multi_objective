import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3] # alternate / sequential

# error weights
result_count = []
# counterexample types
counterexample_type = {}
lines = infile.readlines()
infile.close()

for i in range(len(lines)):
    if mode == 'multi':
        if 'RHO' in lines[i]:
            line = lines[i+1].strip().split(' ')
            val = []
            for s in line:
                if s != '':
                    val.append(float(s) < 0)
            assert len(val) == 13, 'Invalid length of rho'
            result_count.append((val[0] + val[1] + val[2] + val[3] + val[4] + val[5])*128 + (val[6] + val[7] + val[8] + val[9])*8 + val[10] + val[11] + val[12])
            if tuple(1*np.array([val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10], val[11], val[12]])) in counterexample_type:
                counterexample_type[tuple(1*np.array([val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10], val[11], val[12]]))] += 1
            else:
                counterexample_type[tuple(1*np.array([val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10], val[11], val[12]]))] = 1

print('Error weights:', result_count)
print('average:', float(sum(result_count)/len(result_count)), 'max:', np.max(result_count), 'percentage:', float(np.count_nonzero(result_count)/len(result_count)))

print('\nCounterexample types')
print('Types:', len(counterexample_type))
for key, value in reversed(sorted(counterexample_type.items(), key=lambda x: x[0])):
    print("{} : {}".format(key, value))
print()
