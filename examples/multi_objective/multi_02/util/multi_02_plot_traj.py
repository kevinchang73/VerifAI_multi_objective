import matplotlib.pyplot as plt
import sys
import numpy as np

freq = 10
f = open(sys.argv[1], 'r')
lines = f.readlines()

lane_x = []
lane_y = []
ego_pos_x =[]
ego_pos_y =[]
v1_pos_x = []
v1_pos_y = []
v2_pos_x = []
v2_pos_y = []
v3_pos_x = []
v3_pos_y = []

# start lane
num_coords = int(lines[0])
cur_line = 1
for i in range(cur_line, cur_line + num_coords):
    lane_x.append(float(lines[i].split(' ')[0]))
    lane_y.append(float(lines[i].split(' ')[1]))
plt.plot(lane_x, lane_y, 'r', label='_nolegend_', markersize=3)

# end lane
cur_line = cur_line + num_coords
num_coords = int(lines[cur_line])
lane_x = []
lane_y = []
for i in range(cur_line+1, cur_line+1+num_coords):
    lane_x.append(float(lines[i].split(' ')[0]))
    lane_y.append(float(lines[i].split(' ')[1]))
plt.plot(lane_x, lane_y, 'r', label='_nolegend_', markersize=3)

# trajectory
cur_line = cur_line + num_coords + 1
for i in range(cur_line, len(lines)-1):
    if i % freq != 0:
        continue
    ego_pos_x.append(float(lines[i].split(' ')[0]))
    ego_pos_y.append(float(lines[i].split(' ')[1]))
    v1_pos_x.append(float(lines[i].split(' ')[2]))
    v1_pos_y.append(float(lines[i].split(' ')[3]))
    v2_pos_x.append(float(lines[i].split(' ')[4]))
    v2_pos_y.append(float(lines[i].split(' ')[5]))
    v3_pos_x.append(float(lines[i].split(' ')[6]))
    v3_pos_y.append(float(lines[i].split(' ')[7]))

plt.plot(ego_pos_x, ego_pos_y, '-bo', markersize=3)
plt.plot(v1_pos_x, v1_pos_y, '-go', markersize=3)
plt.plot(v2_pos_x, v2_pos_y, '-yo', markersize=3)
plt.plot(v3_pos_x, v3_pos_y, '-co', markersize=3)
plt.plot(ego_pos_x[0], ego_pos_y[0], 'ro', label='_nolegend_', markersize=3)
plt.plot(v1_pos_x[0], v1_pos_y[0], 'ro', label='_nolegend_', markersize=3)
plt.plot(v2_pos_x[0], v2_pos_y[0], 'ro', label='_nolegend_', markersize=3)
plt.plot(v3_pos_x[0], v3_pos_y[0], 'ro', label='_nolegend_', markersize=3)
plt.title('Trajectory')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(['ego', 'v1', 'v2', 'v3'], loc='lower right')
plt.grid(True)
plt.xlim(min(ego_pos_x + v1_pos_x + v2_pos_x + v3_pos_x)-20, max(ego_pos_x + v1_pos_x + v2_pos_x + v3_pos_x)+20)
plt.ylim(min(ego_pos_y + v1_pos_y + v2_pos_y + v3_pos_y)-20, max(ego_pos_y + v1_pos_y + v2_pos_y + v3_pos_y)+20)
plt.show()
plt.savefig(sys.argv[1].split('.')[0]+'.png')
f.close()
