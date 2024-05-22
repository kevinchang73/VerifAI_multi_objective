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
ego_speed = []
dist_threshold = []
blocking_car_dist = []
bypass_dist = []
for file in all_files:
    infile = open(directory+'/'+file, 'r')
    lines = infile.readlines()
    if mode == 'single':
        for i in range(1, len(lines)):
            line = lines[i]
            if float(line.split(',')[-1]) < 0 or float(line.split(',')[-2]) < 0:
                ego_speed.append(float(line.split(',')[-3]))
                dist_threshold.append(float(line.split(',')[-4]))
                bypass_dist.append(float(line.split(',')[-5]))
                blocking_car_dist.append(float(line.split(',')[-6]))
    else:
        for i in range(1, len(lines), 3):
            line1 = lines[i]
            line2 = lines[i+1]
            line3 = lines[i+2]
            if float(line1.split(',')[-1]) < 0 or float(line1.split(',')[-2]) < 0 or float(line2.split(',')[-1]) < 0 or float(line2.split(',')[-2]) < 0 or float(line3.split(',')[-2]) < 0:
                ego_speed.append(float(line1.split(',')[-3]))
                dist_threshold.append(float(line1.split(',')[-4]))
                bypass_dist.append(float(line1.split(',')[-5]))
                blocking_car_dist.append(float(line1.split(',')[-6]))
            #else:
            #    print(file, i)

ax.scatter(ego_speed, dist_threshold, bypass_dist)
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('DIST_THRESHOLD')
ax.set_zlabel('BYPASS_DIST')
plt.savefig(directory+'/'+sys.argv[2]+'_scatter.png')

print("Standard deviation of ego_speed:", np.std(ego_speed), len(ego_speed))
print("Standard deviation of dist_threshold:", np.std(dist_threshold), len(dist_threshold))
print("Standard deviation of bypass_dist:", np.std(bypass_dist), len(bypass_dist))
print("Standard deviation of blocking_car_dist:", np.std(blocking_car_dist), len(blocking_car_dist))
print()
