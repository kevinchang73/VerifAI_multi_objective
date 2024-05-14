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
adv1_speed = []
adv2_speed = []
adv_speed = []
ego_speed = []
for file in all_files:
    infile = open(directory+'/'+file, 'r')
    lines = infile.readlines()
    if mode == 'single':
        for i in range(1, len(lines)):
            line = lines[i] #TODO: identify the counterexamples
            ego_speed.append(float(line.split(',')[-13]))
            adv_speed.append(float(line.split(',')[-14]))
            adv2_speed.append(float(line.split(',')[-15]))
            adv1_speed.append(float(line.split(',')[-16]))
    else:
        for i in range(1, len(lines), 3):
            line1 = lines[i]
            line2 = lines[i+1]
            line3 = lines[i+2] #TODO: identify the counterexamples
            ego_speed.append(float(line1.split(',')[-13]))
            adv_speed.append(float(line1.split(',')[-14]))
            adv2_speed.append(float(line1.split(',')[-15]))
            adv1_speed.append(float(line1.split(',')[-16]))

ax.scatter(ego_speed, adv_speed, adv2_speed)
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('ADV_SPEED')
ax.set_zlabel('ADV2_SPEED')
plt.savefig(directory+'/'+sys.argv[2]+'_scatter.png')

print("Standard deviation of ego_speed:", np.std(ego_speed), len(ego_speed))
print("Standard deviation of adv_speed:", np.std(adv_speed), len(adv_speed))
print("Standard deviation of adv1_speed:", np.std(adv1_speed), len(adv1_speed))
print("Standard deviation of adv2_speed:", np.std(adv2_speed), len(adv2_speed))
print()
