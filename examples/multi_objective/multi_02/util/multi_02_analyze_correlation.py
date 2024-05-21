import matplotlib.pyplot as plt
import numpy as np
import sys

dir_name = sys.argv[1]

r0 = []
r1 = []
r2 = []
r3 = []

adv3_speed = []
adv_speed = []
ego_brake = []
ego_speed = []

file_names = ['result_multi_02_demab0', 'result_multi_02_dmab0', 'result_multi_02_dce0', 'result_multi_02_demab1', 'result_multi_02_dmab1', 'result_multi_02_dce1', 'result_multi_02_halton', 'result_multi_02_random', 'result_multi_02_udemab']
for file in file_names:
    for i in range(3):
        infile = open(dir_name + file + '.' + str(i) + '.csv', 'r')
        lines = infile.readlines()
        for i in range(1, len(lines), 2):
            line1 = lines[i]
            line2 = lines[i+1]
            r0.append(float(line1.split(',')[-3]))
            r1.append(float(line1.split(',')[-2]))
            r2.append(float(line2.split(',')[-1]))
            r3.append(float(line2.split(',')[-4]))
            ego_speed.append(float(line1.split(',')[-5]))
            ego_brake.append(float(line1.split(',')[-6]))
            adv_speed.append(float(line1.split(',')[-7]))
            adv3_speed.append(float(line1.split(',')[-8]))

#file_names = ['result_multi_02_single']
#for file in file_names:
#    for i in range(3):
#        infile = open(dir_name + file + '.' + str(i) + '.csv', 'r')
#        lines = infile.readlines()
#        for i in range(1, len(lines)):
#            line = lines[i]
#            r0.append(float(line.split(',')[-3]))
#            r1.append(float(line.split(',')[-2]))
#            r2.append(float(line.split(',')[-1]))
#            r3.append(float(line.split(',')[-4]))
#            ego_speed.append(float(line.split(',')[-5]))
#            ego_brake.append(float(line.split(',')[-6]))
#            adv_speed.append(float(line.split(',')[-7]))
#            adv3_speed.append(float(line.split(',')[-8]))

print('length of data', len(r0), len(r1), len(r2), len(r3), len(ego_speed), len(ego_brake), len(adv_speed), len(adv3_speed))
print('Correlations between violation scores:')
corr_rho_rho = np.corrcoef([r0, r1, r2, r3])
for i in range(4):
    for j in range(4):
        print(corr_rho_rho[i][j], end=' ')
    print()

print('Correlations between violation scores and parameters:')
print(np.corrcoef([ego_speed, r0])[1][0], np.corrcoef([ego_speed, r1])[1][0], np.corrcoef([ego_speed, r2])[1][0], np.corrcoef([ego_speed, r3])[1][0])
print(np.corrcoef([ego_brake, r0])[1][0], np.corrcoef([ego_brake, r1])[1][0], np.corrcoef([ego_brake, r2])[1][0], np.corrcoef([ego_brake, r3])[1][0])
print(np.corrcoef([adv_speed, r0])[1][0], np.corrcoef([adv_speed, r1])[1][0], np.corrcoef([adv_speed, r2])[1][0], np.corrcoef([adv_speed, r3])[1][0])
print(np.corrcoef([adv3_speed, r0])[1][0], np.corrcoef([adv3_speed, r1])[1][0], np.corrcoef([adv3_speed, r2])[1][0], np.corrcoef([adv3_speed, r3])[1][0])
