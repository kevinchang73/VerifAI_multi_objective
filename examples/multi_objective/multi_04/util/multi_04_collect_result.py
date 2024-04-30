import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3] # alternate / sequential

result_count_0 = [[] for i in range(3)] # result_count_0[i] = results sampled from sampler i
result_count_1 = [[] for i in range(3)] # result_count_1[i] = results sampled from sampler i
result_count_2 = [[] for i in range(3)] # result_count_2[i] = results sampled from sampler i
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
            assert len(val1) == 11, 'Invalid length of rho'
            print('Rho:', val_print[1], val_print[5], val_print[9], val_print[8])
            result_count_0[curr_source].append(val1[1]*8 + val1[5]*4 + val1[9]*2 + val1[8]*1)

            line = lines[i+2].strip().split(' ')
            val2 = []
            for s in line:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 11, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[0]*64 + val2[1]*16 + val2[2]*16 + val2[3]*4 + val2[4]*4 + val2[5]*2 + val2[10]*1)

            line = lines[i+3].strip().split(' ')
            val3 = []
            for s in line:
                if s != '':
                    val3.append(float(s) < 0)
            assert len(val3) == 11, 'Invalid length of rho'
            result_count_2[curr_source].append(val3[2]*4 + val3[3]*4 + val3[4]*4 + val3[5]*2 + val3[8]*1)

            if order == 'alternate':
                curr_source = curr_source + 1 if curr_source < 2 else 0
    else:
        if 'Actual rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[')+1:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 4, 'Invalid length of rho'
            result_count_0[curr_source][val1[0]*2 + val1[1]*1] += 1

            seg2 = line[line.find('] [')+3:-1].split(' ')
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 4, 'Invalid length of rho'
            result_count_1[curr_source][val2[2]*2 + val2[3]] += 1

print('Falsification result in segment 0:')
for i in range(3):
    print('from sampler', i, ':', result_count_0[i])
print('Falsification result in segment 1:')
for i in range(3):
    print('from sampler', i, ':', result_count_1[i])
print('Falsification result in segment 2:')
for i in range(3):
    print('from sampler', i, ':', result_count_2[i])            
#rows = ['from sampler 0', 'from sampler 1']
#cols = ['(r0, r1) = 00', '(r0, r1) = 01', '(r0, r1) = 10', '(r0, r1) = 11']
#df = pd.DataFrame(result_count_0, columns=cols, index=rows)
#print('Falsification result in segment 0:\n', df, '\n')
#cols = ['(r2, r3) = 00', '(r2, r3) = 01', '(r2, r3) = 10', '(r2, r3) = 11']
#df = pd.DataFrame(result_count_1, columns=cols, index=rows)
#print('Falsification result in segment 1:\n', df)
