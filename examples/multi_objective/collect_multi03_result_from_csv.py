import sys
import matplotlib.pyplot as plt

infile = open(sys.argv[1], 'r') # *.csv
lines = infile.readlines()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
count = 0
xs = []
ys = []
zs = []
for i in range(1, len(lines)):
    line = lines[i]
    if float(line.split(',')[-1]) < 0 or float(line.split(',')[-2]) < 0 or float(line.split(',')[-3]) < 0:
        xs.append(float(line.split(',')[-5]))
        ys.append(float(line.split(',')[-6]))
        zs.append(float(line.split(',')[-7]))

ax.scatter(xs, ys, zs)
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('EGO_BRAKE')
ax.set_zlabel('ADV_SPEED')

plt.savefig(sys.argv[1].split('.')[0]+'_scatter.png')
