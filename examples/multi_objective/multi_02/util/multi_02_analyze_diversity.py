import sys
import matplotlib.pyplot as plt
import numpy as np
import os

directory = sys.argv[1]
all_files = os.listdir(directory)
all_files = [f for f in all_files if f.endswith('.csv') and f.startswith(sys.argv[2]+'.')]
mode = sys.argv[3] # multi / single

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
count = 0
adv3_speed = []
adv_speed = []
ego_brake = []
ego_speed = []
adv3_speed_seg0_max = []
adv_speed_seg0_max = []
ego_brake_seg0_max = []
ego_speed_seg0_max = []
for file in all_files:
    infile = open(directory+'/'+file, 'r')
    lines = infile.readlines()
    if mode == 'single':
        for i in range(1, len(lines)):
            line = lines[i]
            if float(line.split(',')[-1]) < 0 or float(line.split(',')[-2]) < 0 or float(line.split(',')[-3]) < 0 or float(line.split(',')[-4]) < 0:
                ego_speed.append(float(line.split(',')[-5]))
                ego_brake.append(float(line.split(',')[-6]))
                adv_speed.append(float(line.split(',')[-7]))
                adv3_speed.append(float(line.split(',')[-8]))
    else:
        for i in range(1, len(lines), 2):
            line1 = lines[i]
            line2 = lines[i+1]
            if float(line1.split(',')[-3]) < 0 and float(line1.split(',')[-2]) < 0:
                ego_speed_seg0_max.append(float(line1.split(',')[-5]))
                ego_brake_seg0_max.append(float(line1.split(',')[-6]))
                adv_speed_seg0_max.append(float(line1.split(',')[-7]))
                adv3_speed_seg0_max.append(float(line1.split(',')[-8]))
            elif float(line1.split(',')[-3]) < 0 or float(line1.split(',')[-2]) < 0 or float(line2.split(',')[-1]) < 0 or float(line2.split(',')[-4]) < 0:
                ego_speed.append(float(line1.split(',')[-5]))
                ego_brake.append(float(line1.split(',')[-6]))
                adv_speed.append(float(line1.split(',')[-7]))
                adv3_speed.append(float(line1.split(',')[-8]))
            else:
                print(file, i)

ax.scatter(ego_speed_seg0_max, ego_brake_seg0_max, adv_speed_seg0_max, c='r')
ax.scatter(ego_speed, ego_brake, adv_speed, c='b')
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('EGO_BRAKE')
ax.set_zlabel('ADV_SPEED')
plt.savefig(directory+'/'+sys.argv[2]+'_scatter.png')

print("Standard deviation of ego_speed:", np.std(ego_speed), len(ego_speed))
print("Standard deviation of ego_brake:", np.std(ego_brake), len(ego_brake))
print("Standard deviation of adv_speed:", np.std(adv_speed), len(adv_speed))
print("Standard deviation of adv3_speed:", np.std(adv3_speed), len(adv3_speed))
print()
