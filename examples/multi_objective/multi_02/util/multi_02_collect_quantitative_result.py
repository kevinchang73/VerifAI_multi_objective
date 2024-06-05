import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dir_name = sys.argv[1]

print("Segment 0")
file_names = ['result_multi_02_demab0_0.log', 'result_multi_02_dmab0.log', 'result_multi_02_dce0.log', 'result_multi_02_halton.log', 'result_multi_02_random.log', 'result_multi_02_udemab.log']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    r0 = []
    r1 = []
    for i in range(len(lines)):
        if 'Rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[[')+2:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s))
            assert len(val1) == 4, 'Invalid length of rho'
            r0.append(val1[0])
            r1.append(val1[1])
            #if val1[0] < 0:
            #    r0.append(val1[0])
            #else:
            #    r0.append(0)
            #if val1[1] < 0:
            #    r1.append(val1[1])
            #else:
            #    r1.append(0)
    r0 = np.array(r0)
    r1 = np.array(r1)
    r0_neg = np.array([r for r in r0 if r < 0])
    r1_neg = np.array([r for r in r1 if r < 0])
    print(np.mean(r0), np.mean(r0_neg), np.min(r0), np.max(r0), np.mean(r1), np.mean(r1_neg), np.min(r1), np.max(r1))

'''
file_names = ['result_multi_02_single.log']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    r0 = []
    r1 = []
    for i in range(len(lines)):
        if 'Actual rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[')+1:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s))
            assert len(val1) == 4, 'Invalid length of rho'
            if val1[0] < 0:
                r0.append(val1[0])
            else:
                r0.append(0)
            if val1[1] < 0:
                r1.append(val1[1])
            else:
                r1.append(0)
    print(file)
    print('r0', 'mean:', np.mean(r0), 'min:', np.min(r0), 'len:', len(r0))
    print('r1', 'mean:', np.mean(r1), 'min:', np.min(r1), 'len:', len(r1))
'''

print("\nSegment 1")
file_names = ['result_multi_02_demab1.log', 'result_multi_02_dmab1.log', 'result_multi_02_dce1.log', 'result_multi_02_halton.log', 'result_multi_02_random.log', 'result_multi_02_udemab.log']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    r2 = []
    r3 = []
    for i in range(len(lines)):
        if 'Rho' in lines[i]:
            line = lines[i+1].strip()
            seg2 = line[line.find('[')+1:line.find(']]')].split(' ')
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s))
            assert len(val2) == 4, 'Invalid length of rho'
            r2.append(val2[2])
            r3.append(val2[3])
            #if val2[2] < 0:
            #    r2.append(val2[2])
            #else:
            #    r2.append(0)
            #if val2[3] < 0:
            #    r3.append(val2[3])
            #else:
            #    r3.append(0)
    r2 = np.array(r2)
    r3 = np.array(r3)
    r2_neg = np.array([r for r in r2 if r < 0])
    r3_neg = np.array([r for r in r3 if r < 0])
    print(np.mean(r2), np.mean(r2_neg), np.min(r2), np.max(r2), np.mean(r3), np.mean(r3_neg), np.min(r3), np.max(r3))

'''
file_names = ['result_multi_02_single.log']
for file in file_names:
    f = open(dir_name + file, 'r')
    lines = f.readlines()
    f.close()

    r2 = []
    r3 = []
    if 'Actual rho' in lines[i]:
        line = lines[i].strip()
        seg2 = line[line.find('] [')+3:-1].split(' ')
        val2 = []
        for s in seg2:
            if s != '':
                val2.append(float(s))
        assert len(val2) == 4, 'Invalid length of rho'
        if val2[2] < 0:
            r2.append(val2[2])
        else:
            r2.append(0)
        if val2[3] < 0:
            r3.append(val2[3])
        else:
            r3.append(0)
    print(file)
    print('r2', 'mean:', np.mean(r2), 'min:', np.min(r2), 'len:', len(r2))
    print('r3', 'mean:', np.mean(r3), 'min:', np.min(r3), 'len:', len(r3))
'''