import matplotlib.pyplot as plt
import numpy as np
import sys

dir_name = sys.argv[1]

r1_0 = []
r5_0 = []
r8_0 = []
r9_0 = []
r0_1 = []
r1_1 = []
r2_1 = []
r3_1 = []
r4_1 = []
r5_1 = []
r10_1 = []
r2_2 = []
r3_2 = []
r4_2 = []
r5_2 = []
r8_2 = []

adv1_speed = []
adv2_speed = []
adv_speed = []
ego_speed = []
weather = []

file_names = ['result_multi_04_demab0', 'result_multi_04_dmab0', 'result_multi_04_demab1', 'result_multi_04_demab2', 'result_multi_04_dmab2', 'result_multi_04_random']
for file in file_names:
    for i in range(3):
        infile = open(dir_name + file + '.' + str(i) + '.csv', 'r')
        lines = infile.readlines()
        for i in range(1, len(lines), 3):
            line1 = lines[i]
            line2 = lines[i+1]
            line3 = lines[i+2]

            r1_0.append(float(line1.split(',')[-9]))
            r5_0.append(float(line1.split(',')[-5]))
            r8_0.append(float(line1.split(',')[-2]))
            r9_0.append(float(line1.split(',')[-1]))
            r0_1.append(float(line2.split(',')[-10]))
            r1_1.append(float(line2.split(',')[-9]))
            r2_1.append(float(line2.split(',')[-8]))
            r3_1.append(float(line2.split(',')[-7]))
            r4_1.append(float(line2.split(',')[-6]))
            r5_1.append(float(line2.split(',')[-5]))
            r10_1.append(float(line2.split(',')[-11]))
            r2_2.append(float(line3.split(',')[-8]))
            r3_2.append(float(line3.split(',')[-7]))
            r4_2.append(float(line3.split(',')[-6]))
            r5_2.append(float(line3.split(',')[-5]))
            r8_2.append(float(line3.split(',')[-2]))

            weather.append(float(line1.split(',')[-12]))
            ego_speed.append(float(line1.split(',')[-13]))
            adv_speed.append(float(line1.split(',')[-14]))
            adv2_speed.append(float(line1.split(',')[-15]))
            adv1_speed.append(float(line1.split(',')[-16]))

#file_names = ['result_multi_04_single']
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

print('length of data', len(r1_0), len(ego_speed))
print('Correlations between violation scores:')
corr_rho_rho = np.corrcoef([r1_0, r5_0, r8_0, r9_0, r0_1, r1_1, r2_1, r3_1, r4_1, r5_1, r10_1, r2_2, r3_2, r4_2, r5_2, r8_2])
for i in range(16):
    for j in range(16):
        print(corr_rho_rho[i][j], end=' ')
    print()

print('Correlations between violation scores and parameters:')
print(np.corrcoef([ego_speed, r1_0])[1][0], np.corrcoef([ego_speed, r5_0])[1][0], np.corrcoef([ego_speed, r8_0])[1][0], np.corrcoef([ego_speed, r9_0])[1][0], np.corrcoef([ego_speed, r0_1])[1][0], np.corrcoef([ego_speed, r1_1])[1][0], np.corrcoef([ego_speed, r2_1])[1][0], np.corrcoef([ego_speed, r3_1])[1][0], np.corrcoef([ego_speed, r4_1])[1][0], np.corrcoef([ego_speed, r5_1])[1][0], np.corrcoef([ego_speed, r10_1])[1][0], np.corrcoef([ego_speed, r2_2])[1][0], np.corrcoef([ego_speed, r3_2])[1][0], np.corrcoef([ego_speed, r4_2])[1][0], np.corrcoef([ego_speed, r5_2])[1][0], np.corrcoef([ego_speed, r8_2])[1][0])
print(np.corrcoef([adv_speed, r1_0])[1][0], np.corrcoef([adv_speed, r5_0])[1][0], np.corrcoef([adv_speed, r8_0])[1][0], np.corrcoef([adv_speed, r9_0])[1][0], np.corrcoef([adv_speed, r0_1])[1][0], np.corrcoef([adv_speed, r1_1])[1][0], np.corrcoef([adv_speed, r2_1])[1][0], np.corrcoef([adv_speed, r3_1])[1][0], np.corrcoef([adv_speed, r4_1])[1][0], np.corrcoef([adv_speed, r5_1])[1][0], np.corrcoef([adv_speed, r10_1])[1][0], np.corrcoef([adv_speed, r2_2])[1][0], np.corrcoef([adv_speed, r3_2])[1][0], np.corrcoef([adv_speed, r4_2])[1][0], np.corrcoef([adv_speed, r5_2])[1][0], np.corrcoef([adv_speed, r8_2])[1][0])
print(np.corrcoef([adv2_speed, r1_0])[1][0], np.corrcoef([adv2_speed, r5_0])[1][0], np.corrcoef([adv2_speed, r8_0])[1][0], np.corrcoef([adv2_speed, r9_0])[1][0], np.corrcoef([adv2_speed, r0_1])[1][0], np.corrcoef([adv2_speed, r1_1])[1][0], np.corrcoef([adv2_speed, r2_1])[1][0], np.corrcoef([adv2_speed, r3_1])[1][0], np.corrcoef([adv2_speed, r4_1])[1][0], np.corrcoef([adv2_speed, r5_1])[1][0], np.corrcoef([adv2_speed, r10_1])[1][0], np.corrcoef([adv2_speed, r2_2])[1][0], np.corrcoef([adv2_speed, r3_2])[1][0], np.corrcoef([adv2_speed, r4_2])[1][0], np.corrcoef([adv2_speed, r5_2])[1][0], np.corrcoef([adv2_speed, r8_2])[1][0])
print(np.corrcoef([adv1_speed, r1_0])[1][0], np.corrcoef([adv1_speed, r5_0])[1][0], np.corrcoef([adv1_speed, r8_0])[1][0], np.corrcoef([adv1_speed, r9_0])[1][0], np.corrcoef([adv1_speed, r0_1])[1][0], np.corrcoef([adv1_speed, r1_1])[1][0], np.corrcoef([adv1_speed, r2_1])[1][0], np.corrcoef([adv1_speed, r3_1])[1][0], np.corrcoef([adv1_speed, r4_1])[1][0], np.corrcoef([adv1_speed, r5_1])[1][0], np.corrcoef([adv1_speed, r10_1])[1][0], np.corrcoef([adv1_speed, r2_2])[1][0], np.corrcoef([adv1_speed, r3_2])[1][0], np.corrcoef([adv1_speed, r4_2])[1][0], np.corrcoef([adv1_speed, r5_2])[1][0], np.corrcoef([adv1_speed, r8_2])[1][0])
print(np.corrcoef([weather, r1_0])[1][0], np.corrcoef([weather, r5_0])[1][0], np.corrcoef([weather, r8_0])[1][0], np.corrcoef([weather, r9_0])[1][0], np.corrcoef([weather, r0_1])[1][0], np.corrcoef([weather, r1_1])[1][0], np.corrcoef([weather, r2_1])[1][0], np.corrcoef([weather, r3_1])[1][0], np.corrcoef([weather, r4_1])[1][0], np.corrcoef([weather, r5_1])[1][0], np.corrcoef([weather, r10_1])[1][0], np.corrcoef([weather, r2_2])[1][0], np.corrcoef([weather, r3_2])[1][0], np.corrcoef([weather, r4_2])[1][0], np.corrcoef([weather, r5_2])[1][0], np.corrcoef([weather, r8_2])[1][0])
