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
speed = []
brake = []
arrving_dist = []

for file in all_files:
    infile = open(directory+'/'+file, 'r')
    lines = infile.readlines()
    for i in range(1, len(lines)):
        line = lines[i]
        rhos = np.array(line.split(',')[-13:-1]).astype(float)
        if np.any(rhos < 0):
            speed.append(float(line.split(',')[-14]))
            brake.append(float(line.split(',')[-15]))
            arrving_dist.append(float(line.split(',')[-16]))

ax.scatter(speed, brake, arrving_dist)
ax.set_xlabel('SPEED')
ax.set_ylabel('BRAKE')
ax.set_zlabel('ARRIVING DISTANCE')
plt.savefig(directory+'/'+sys.argv[2]+'_scatter.png')

print("Standard deviation of speed:", np.std(speed))
print("Standard deviation of brake:", np.std(brake))
print("Standard deviation of arrving_dist:", np.std(arrving_dist))
print()
