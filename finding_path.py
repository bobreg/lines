import random

pole_path = [['x' for i in range(11)] for j in range(11)]

for i in range(1, 10):
    for j in range(1, 10):
        pole_path[i][j] = random.randrange(0, -2, -1)

#for i in range(1, 9):
    #for j in range(1, 9):
        #pole_path[i][j] = 0

for i in range(1, 10):
    for j in range(1, 10):
        if pole_path[i][j] == -1:
            pole_path[i][j] = 'x'
for i in range(11):
    print(pole_path[i])
pole_path[4][4] = 1
pole_path[6][6] = 0
iteratinon = 0

while iteratinon < 100:  # поиск пути версия первая. Ищется только возможность пути
    for i in range(1, 10):
        for j in range(1, 10):
            if pole_path[i][j + 1] != 'x' and pole_path[i][j + 1] == 0 and pole_path[i][j] != 'x':
                pole_path[i][j + 1] = pole_path[i][j] + pole_path[i][j + 1]
    for i in range(1, 10):
        for j in range(1, 10):
            if pole_path[i - 1][j] != 'x' and pole_path[i - 1][j] == 0 and pole_path[i][j] != 'x':
                pole_path[i - 1][j] = pole_path[i][j] + pole_path[i - 1][j]
    for i in range(1, 10):
        for j in range(1, 10):
            if pole_path[i + 1][j] != 'x' and pole_path[i + 1][j] == 0 and pole_path[i][j] != 'x':
                pole_path[i + 1][j] = pole_path[i][j] + pole_path[i + 1][j]
    for i in range(1, 10):
        for j in range(1, 10):
            if pole_path[i][j - 1] != 'x' and pole_path[i][j - 1] == 0 and pole_path[i][j] != 'x':
                pole_path[i][j - 1] = pole_path[i][j] + pole_path[i][j - 1]
    iteratinon += 1

for i in range(11):
    for j in range(11):
        pole_path[i][j] = str(pole_path[i][j])

for i in range(11):
    print(' '.join(pole_path[i]))
