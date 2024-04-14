import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3] # alternate / sequential

result_count_0 = np.zeros(shape=(4,8), dtype=int) # result_count_0[i] = [count of 000, 001, 010, 011, 100, 101, 110, 111 in segment 0] sampled from sampler i
result_count_1 = np.zeros(shape=(4,8), dtype=int) # result_count_1[i] = [count of 000, 001, 010, 011, 100, 101, 110, 111 in segment 1] sampled from sampler i
result_count_2 = np.zeros(shape=(4,8), dtype=int) # result_count_2[i] = [count of 000, 001, 010, 011, 100, 101, 110, 111 in segment 2] sampled from sampler i
result_count_3 = np.zeros(shape=(4,8), dtype=int) # result_count_3[i] = [count of 000, 001, 010, 011, 100, 101, 110, 111 in segment 3] sampled from sampler i
curr_source = 0
lines = infile.readlines()
infile.close()

for i in range(len(lines)):
    if mode == 'multi':
        if 'Rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[[')+2:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 3, 'Invalid length of rho'
            result_count_0[curr_source][val1[0]*4 + val1[1]*2 + val1[2]] += 1

            line = lines[i+1].strip()
            seg2 = line[line.find('[')+1:line.find(']')].split(' ')
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 3, 'Invalid length of rho'
            result_count_1[curr_source][val2[0]*4 + val2[1]*2 + val2[2]] += 1

            line = lines[i+2].strip()
            seg3 = line[line.find('[')+1:line.find(']')].split(' ')
            val3 = []
            for s in seg3:
                if s != '':
                    val3.append(float(s) < 0)
            assert len(val3) == 3, 'Invalid length of rho'
            result_count_2[curr_source][val3[0]*4 + val3[1]*2 + val3[2]] += 1

            line = lines[i+3].strip()
            seg4 = line[line.find('[')+1:line.find(']')].split(' ')
            val4 = []
            for s in seg4:
                if s != '':
                    val4.append(float(s) < 0)
            assert len(val4) == 3, 'Invalid length of rho'
            result_count_3[curr_source][val4[0]*4 + val4[1]*2 + val4[2]] += 1
            
            if order == 'alternate':
                curr_source = (curr_source + 1) % 4
    else:
        if 'Actual rho' in lines[i]:
            line = lines[i].strip()
            line = line[line.find('[')+1:]
            line = line.replace('[', '').replace(']', '').split(' ')
            line = [s for s in line if s != '']

            seg1 = line[0:3]
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 3, 'Invalid length of rho'
            result_count_0[curr_source][val1[0]*4 + val1[1]*2 + val1[2]] += 1

            seg2 = line[3:6]
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 3, 'Invalid length of rho'
            result_count_1[curr_source][val2[0]*4 + val2[1]*2 + val2[2]] += 1

            seg3 = line[6:9]
            val3 = []
            for s in seg3:
                if s != '':
                    val3.append(float(s) < 0)
            assert len(val3) == 3, 'Invalid length of rho'
            result_count_2[curr_source][val3[0]*4 + val3[1]*2 + val3[2]] += 1

            seg4 = line[9:12]
            val4 = []
            for s in seg4:
                if s != '':
                    val4.append(float(s) < 0)
            assert len(val4) == 3, 'Invalid length of rho'
            result_count_3[curr_source][val4[0]*4 + val4[1]*2 + val4[2]] += 1
            
rows = ['from sampler 0', 'from sampler 1', 'from sampler 2', 'from sampler 3']
cols = ['000', '001', '010', '011', '100', '101', '110', '111']
df = pd.DataFrame(result_count_0, columns=cols, index=rows)
print('Falsification result in segment 0:\n', df, '\n')
df = pd.DataFrame(result_count_1, columns=cols, index=rows)
print('Falsification result in segment 1:\n', df, '\n')
df = pd.DataFrame(result_count_2, columns=cols, index=rows)
print('Falsification result in segment 2:\n', df, '\n')
df = pd.DataFrame(result_count_3, columns=cols, index=rows)
print('Falsification result in segment 3:\n', df)
