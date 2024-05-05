import sys
import matplotlib.pyplot as plt
import numpy as np

infile = open(sys.argv[1], 'r') # *.csv
lines = infile.readlines()
mode = sys.argv[2] # multi / single

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
count = 0
adv3_speed = []
adv_speed = []
ego_brake = []
ego_speed = []
if mode == 'single':
    for i in range(1, len(lines)):
        line = lines[i]
        if float(line.split(',')[-1]) < 0 or float(line.split(',')[-2]) < 0 or float(line.split(',')[-3]) < 0:
            ego_speed.append(float(line.split(',')[-5]))
            ego_brake.append(float(line.split(',')[-6]))
            adv_speed.append(float(line.split(',')[-7]))
            adv3_speed.append(float(line.split(',')[-8]))
else:
    for i in range(1, len(lines), 2):
        line1 = lines[i]
        line2 = lines[i+1]
        if float(line1.split(',')[-1]) < 0 or float(line1.split(',')[-2]) < 0 or float(line2.split(',')[-3]) < 0 or float(line2.split(',')[-4]) < 0:
            ego_speed.append(float(line1.split(',')[-5]))
            ego_brake.append(float(line1.split(',')[-6]))
            adv_speed.append(float(line1.split(',')[-7]))
            adv3_speed.append(float(line1.split(',')[-8]))

ax.scatter(ego_speed, ego_brake, adv_speed)
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('EGO_BRAKE')
ax.set_zlabel('ADV_SPEED')
plt.savefig(sys.argv[1].split('.')[0]+'_scatter.png')

print("Variance of ego_speed:", np.var(ego_speed))
print("Variance of ego_brake:", np.var(ego_brake))
print("Variance of adv_speed:", np.var(adv_speed))
print("Variance of adv3_speed:", np.var(adv3_speed))
print()
