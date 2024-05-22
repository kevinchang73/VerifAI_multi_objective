import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3]

# error weights
result_count_0 = [[] for i in range(3)]
result_count_1 = [[] for i in range(3)]
result_count_2 = [[] for i in range(3)]
# counterexample types
counterexample_type_0 = [{} for i in range(3)]
counterexample_type_1 = [{} for i in range(3)]
counterexample_type_2 = [{} for i in range(3)]
curr_source = 0
lines = infile.readlines()
infile.close()

for i in range(len(lines)):
    if mode == 'multi':
        if 'RHO' in lines[i]:
            line = lines[i+1].strip().split(' ')
            val1 = []
            val_print = []
            for s in line:
                if s != '':
                    val1.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val1) == 2, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*1 + val1[1]*2)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1

            line = lines[i+2].strip().split(' ')
            val2 = []
            val_print = []
            for s in line:
                if s != '':
                    val2.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val2) == 2, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[0]*2 + val2[1]*1)
            if tuple(1*np.array([val2[0], val2[1]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[0], val2[1]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[0], val2[1]]))] = 1

            line = lines[i+3].strip().split(' ')
            val3 = []
            val_print = []
            for s in line:
                if s != '':
                    val3.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val3) == 2, 'Invalid length of rho'
            result_count_2[curr_source].append(val3[1]*1)
            if tuple(1*np.array([val3[1]])) in counterexample_type_2[curr_source]:
                counterexample_type_2[curr_source][tuple(1*np.array([val3[1]]))] += 1
            else:
                counterexample_type_2[curr_source][tuple(1*np.array([val3[1]]))] = 1

            if order == '-1':
                curr_source = curr_source + 1 if curr_source < 2 else 0
    else:
        if 'Actual rho' in lines[i]:
            line = lines[i+1].strip().split(' ')
            val1 = []
            val_print = []
            for s in line:
                if s != '':
                    val1.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val1) == 2, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*1 + val1[1]*2)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1

            line = lines[i+2].strip().split(' ')
            val2 = []
            val_print = []
            for s in line:
                if s != '':
                    val2.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val2) == 2, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[0]*2 + val2[1]*1)
            if tuple(1*np.array([val2[0], val2[1]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[0], val2[1]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[0], val2[1]]))] = 1

            line = lines[i+3].strip().split(' ')
            val3 = []
            val_print = []
            for s in line:
                if s != '':
                    val3.append(float(s) < 0)
                    val_print.append(float(s))
            assert len(val3) == 2, 'Invalid length of rho'
            result_count_2[curr_source].append(val3[1]*1)
            if tuple(1*np.array([val3[1]])) in counterexample_type_2[curr_source]:
                counterexample_type_2[curr_source][tuple(1*np.array([val3[1]]))] += 1
            else:
                counterexample_type_2[curr_source][tuple(1*np.array([val3[1]]))] = 1

            if order == '-1':
                curr_source = curr_source + 1 if curr_source < 2 else 0

print('Error weights')
print('segment 0:')
for i in range(1):
    print('average:', np.mean(result_count_0[i]), 'max:', np.max(result_count_0[i]), 'percentage:', float(np.count_nonzero(result_count_0[i])/len(result_count_0[i])), result_count_0[i])
print('segment 1:')
for i in range(1):
    print('average:', np.mean(result_count_1[i]), 'max:', np.max(result_count_1[i]), 'percentage:', float(np.count_nonzero(result_count_1[i])/len(result_count_1[i])), result_count_1[i])
print('segment 2:')
for i in range(1):
    print('average:', np.mean(result_count_2[i]), 'max:', np.max(result_count_2[i]), 'percentage:', float(np.count_nonzero(result_count_2[i])/len(result_count_2[i])), result_count_2[i])

print('\nCounterexample types')
print('segment 0:')
for i in range(1):
    print('Types:', len(counterexample_type_0[i]))
    for key, value in reversed(sorted(counterexample_type_0[i].items(), key=lambda x: x[0])):
        print("{} : {}".format(key, value))
print('segment 1:')
for i in range(1):
    print('Types:', len(counterexample_type_1[i]))
    for key, value in reversed(sorted(counterexample_type_1[i].items(), key=lambda x: x[0])):
        print("{} : {}".format(key, value))
print('segment 2:')
for i in range(1):
    print('Types:', len(counterexample_type_2[i]))
    for key, value in reversed(sorted(counterexample_type_2[i].items(), key=lambda x: x[0])):
        print("{} : {}".format(key, value))
print()
