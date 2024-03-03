import sys
import matplotlib.pyplot as plt
import numpy as np

infile = open(sys.argv[1], 'r') # *.txt
lines = infile.readlines()

falsiResultCount000 = 0
falsiResultCount001 = 0
falsiResultCount010 = 0
falsiResultCount011 = 0
falsiResultCount100 = 0
falsiResultCount101 = 0
falsiResultCount110 = 0
falsiResultCount111 = 0

count = 0
time = []
error = []
Q_ratio = []
for i in range(len(lines)):
    line = lines[i]
    # count each case / add line chart points
    if 'Result' in line:
        count += 1
        time.append(count)
        if line.split(' ')[2] == 'False' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'False\n':
            falsiResultCount000 = falsiResultCount000 + 1
            error.append(0)
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'True\n':
            falsiResultCount001 = falsiResultCount001 + 1
            error.append(1)
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'False\n':
            falsiResultCount010 = falsiResultCount010 + 1
            error.append(2)
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'True\n':
            falsiResultCount011 = falsiResultCount011 + 1
            error.append(3)
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'False\n':
            falsiResultCount100 = falsiResultCount100 + 1
            error.append(4)
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'True\n':
            falsiResultCount101 = falsiResultCount101 + 1
            error.append(5)
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'False\n':
            falsiResultCount110 = falsiResultCount110 + 1
            error.append(6)
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'True\n':
            falsiResultCount111 = falsiResultCount111 + 1
            error.append(7)
    
    # Q ratio
    if 'Q' in line:
        #print(line.split(' ')[2].split('[')[-1], line.split(' ')[3], line.split(' ')[4], line.split(' ')[5], line.split(' ')[6].split(']')[0])
        temp_list = [float(line.split(' ')[2].split('[')[-1]), float(line.split(' ')[3]), float(line.split(' ')[4]), float(line.split(' ')[5]), float(line.split(' ')[6].split(']')[0])]
        argmax1 = np.argmax(temp_list)
        temp_list = [float(lines[i+1].split(' ')[1].split('[')[-1]), float(lines[i+1].split(' ')[2]), float(lines[i+1].split(' ')[3]), float(lines[i+1].split(' ')[4]), float(lines[i+1].split(' ')[5].split(']')[0])]
        argmax2 = np.argmax(temp_list)
        temp_list = [float(lines[i+2].split(' ')[1].split('[')[-1]), float(lines[i+2].split(' ')[2]), float(lines[i+2].split(' ')[3]), float(lines[i+2].split(' ')[4]), float(lines[i+2].split(' ')[5].split(']')[0])]
        argmax3 = np.argmax(temp_list)
        temp_list = [float(lines[i+3].split(' ')[1].split('[')[-1]), float(lines[i+3].split(' ')[2]), float(lines[i+3].split(' ')[3]), float(lines[i+3].split(' ')[4]), float(lines[i+3].split(' ')[5].split(']')[0])]
        argmax4 = np.argmax(temp_list)

        average = 0
        temp_list = [float(lines[i+12].split(' ')[2].split('[')[-1]), float(lines[i+12].split(' ')[3]), float(lines[i+12].split(' ')[4]), float(lines[i+12].split(' ')[5]), float(lines[i+12].split(' ')[6].split(']')[0])]
        average += temp_list[argmax1]
        temp_list = [float(lines[i+13].split(' ')[1].split('[')[-1]), float(lines[i+13].split(' ')[2]), float(lines[i+13].split(' ')[3]), float(lines[i+13].split(' ')[4]), float(lines[i+13].split(' ')[5].split(']')[0])]
        average += temp_list[argmax2]
        temp_list = [float(lines[i+14].split(' ')[1].split('[')[-1]), float(lines[i+14].split(' ')[2]), float(lines[i+14].split(' ')[3]), float(lines[i+14].split(' ')[4]), float(lines[i+14].split(' ')[5].split(']')[0])]
        average += temp_list[argmax3]
        temp_list = [float(lines[i+15].split(' ')[1].split('[')[-1]), float(lines[i+15].split(' ')[2]), float(lines[i+15].split(' ')[3]), float(lines[i+15].split(' ')[4]), float(lines[i+15].split(' ')[5].split(']')[0])]
        average += temp_list[argmax4]
        average = average / 4.0
        Q_ratio.append(average)
        #print(temp_list, argmax)

print(falsiResultCount111, falsiResultCount110, falsiResultCount101, falsiResultCount100, falsiResultCount011, falsiResultCount010, falsiResultCount001, falsiResultCount000)

# calculate window average
window_size = 20
moving_averages = []
i = 0
while i < len(error) - window_size + 1:
    window = error[i : i + window_size]
    window_average = round(sum(window) / window_size, 2)
    moving_averages.append(window_average)
    i += 1
plt.plot(time[:-window_size+1], moving_averages, 'r')
plt.savefig(sys.argv[1].split('.')[0]+'.png')

fig2 = plt.figure()
ax = fig2.add_subplot()
ax.plot(time[:-1], Q_ratio)
ax.set_xlabel('iteration')
ax.set_ylabel('Q_ratio')
plt.savefig(sys.argv[1].split('.')[0]+'_Qratio.png')