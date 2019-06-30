pole = [[[i, j] for i in range(9)] for j in range(9)]
yy, xx = [int(i) for i in input().split()]
diagonal_y_x = [pole[yy][xx]]
diagonal_y_minus_x = [pole[yy][xx]]
# диагональ у=х
y = yy + 1
x = xx - 1
while y <= 8 and x >= 0:  # добавляем элементы справа налево, сверху вниз
    diagonal_y_x.insert(0, pole[y][x])
    y += 1
    x -= 1

y = yy - 1
x = xx + 1
while x <= 8 and y >= 0:  # добавляем элементы слева направо, снизу вверх
    diagonal_y_x.append(pole[y][x])
    y -= 1
    x += 1
# диагональ у=-х
y = yy - 1
x = xx - 1
while y >= 0 and x >= 0:  # добавляем элементы справа налево, снизу вверх
    diagonal_y_minus_x.insert(0, pole[y][x])
    y -= 1
    x -= 1

y = yy + 1
x = xx + 1
while x <= 8 and y <= 8:  # добавляем элементы слева направо, сверху вниз
    diagonal_y_minus_x.append(pole[y][x])
    y += 1
    x += 1

for i in pole:print(i)
print(diagonal_y_x)
print(diagonal_y_minus_x)
print(pole[yy][xx][0])
