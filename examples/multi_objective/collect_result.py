import sys

infile = open(sys.argv[1], 'r')
lines = infile.readlines()

falsiResultCount000 = 0
falsiResultCount001 = 0
falsiResultCount010 = 0
falsiResultCount011 = 0
falsiResultCount100 = 0
falsiResultCount101 = 0
falsiResultCount110 = 0
falsiResultCount111 = 0

for line in lines:
    if 'Result' in line:
        if line.split(' ')[2] == 'False' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'False\n':
            falsiResultCount000 = falsiResultCount000 + 1
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'True\n':
            falsiResultCount001 = falsiResultCount001 + 1
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'False\n':
            falsiResultCount010 = falsiResultCount010 + 1
        elif line.split(' ')[2] == 'False' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'True\n':
            falsiResultCount011 = falsiResultCount011 + 1
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'False\n':
            falsiResultCount100 = falsiResultCount100 + 1
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'False' and line.split(' ')[4] == 'True\n':
            falsiResultCount101 = falsiResultCount101 + 1
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'False\n':
            falsiResultCount110 = falsiResultCount110 + 1
        elif line.split(' ')[2] == 'True' and line.split(' ')[3] == 'True' and line.split(' ')[4] == 'True\n':
            falsiResultCount111 = falsiResultCount111 + 1

print(falsiResultCount000, falsiResultCount001, falsiResultCount010, falsiResultCount011, falsiResultCount100, falsiResultCount101, falsiResultCount110, falsiResultCount111)
