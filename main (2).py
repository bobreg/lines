import tkinter
import random
import threading
import time

y_shift = 3  # сдвиг для связи матрицы значений и кнопок (кнопки лежат в диапазоне 3-12 по вертикале и 0-9 по горизонтале)
c = 5  # координата для запоминания нажатой кнопки
d = 5  # координата для запоминания нажатой кнопки
flag = False  # флаг для перевыбора другого шарика, чтобы не выбрать два кружка или не перенести выбранный кружок на другой
flag_add_balls = True  # флаг для добавления новых кружков
list_file_static = ['blue-1.gif', 'brown-1.gif', 'green-1.gif', 'pink-1.gif', 'violet-1.gif', 'red-1.gif', 'yellow-1.gif']  # названия файлов кружков
list_file_move = ['blue-24.gif', 'brown-24.gif', 'green-24.gif', 'pink-24.gif', 'violet-24.gif', 'red-24.gif', 'yellow-24.gif']  # названия файлов кружков
colour_choise = 0
next_colours = []
level = 0  # номер кадра gif картинки
animate_x, animate_y = 0, 0
indefikator_animate = 0

pole = [['x' for i in range(9)] for j in range(9)]  # матрица хранения значений кружков


def random_add():  # добавление рандомных трех кружков
    for i in range(3):
        y = random.randrange(0, 9, 1)  # определяем координаты для нового кружка
        x = random.randrange(0, 9, 1)
        while globals()['button{}{}'.format(y+y_shift, x)]['image'] != '': # если они совпали с тем где уже стоит кружок, ищем новое свободное место
            y = random.randrange(0, 9, 1)
            x = random.randrange(0, 9, 1)
        colour = list_colours[next_colours[i]]
        globals()['button{}{}'.format(y+y_shift, x)]['image'] = colour
        globals()['button{}{}'.format(y + y_shift, x)]['width'] = 60
        globals()['button{}{}'.format(y + y_shift, x)]['height'] = 65
        pole[y][x] = list_colours.index(colour)
        proverka_combo(y, x, list_colours.index(colour))
    #for i in range(9): print(pole[i])
    #print('---------------------')


def next_random_colours():
    global next_colours
    next_colours = []
    for i in range(3):
        next_colours += [random.randrange(0, len(list_colours))]


def max_posl(posl, code_colour):  # функция определения максимально длинной последовательности единиц и возвращением координат начала и конца этой последовательности.
    posl_copy = posl[:]  # копия списка нужна чтобы не менялась исходная матрица
    posl_copy.append('x') #добавляем ноль в конце, чтобы алгоритм корректно отработал если последнее значение в массиве 1
    xmin = -1
    xmax = -1
    max_len_one_old = 0
    try:  # а потому что если в массиве одни нули, то будет ошибка, но вообще тут это не нужно
        min_one_index = posl_copy.index(code_colour)  # отсечём лишние нули в начале массива
        i = min_one_index + 1  # начнём со следующего символа после первой найденной единицы
        len_one = 1
        max_len_one = 1
        while min_one_index < len(posl_copy) and i < len(posl_copy):  # работаем до тех пор пока не дойдём до конца массива
            if posl_copy[i] == posl_copy[min_one_index] and posl_copy[min_one_index] == code_colour: #  если следующий символ равен предыдущему и он равен 1, то
                i += 1  # сдвигаем координату дальше
                len_one += 1  # учтём что длительность увеличилась
            else:  # впрочем
                max_len_one = max(max_len_one, len_one)  # сравним новую найденную длинну последовательности со старой и выберем наиболее длинную
                if max_len_one > max_len_one_old:  # сравним старую длинную последовательность с новой найденной, если она изменилась, то
                    xmin = min_one_index  # обновим координаты
                    xmax = i - 1
                    max_len_one_old = max_len_one  # перепишем новую длинну в старую
                min_one_index = i # начнём новый поиск
                i = min_one_index + 1
                len_one = 1
        max_len_one = max(max_len_one, len_one)
        return xmin, xmax
    except ValueError:
        return xmin, xmax


def bild_diagonals(yy, xx):  # функция возвращает массивы из координат диагоналей для переданной клетки
    list_coordinates = [[[i, j] for i in range(9)] for j in range(9)]
    diagonal_y_x = [list_coordinates[yy][xx]]
    diagonal_y_minus_x = [list_coordinates[yy][xx]]
    # диагональ у=х
    y = yy + 1
    x = xx - 1
    while y <= 8 and x >= 0:  # добавляем элементы справа налево, сверху вниз
        diagonal_y_x.insert(0, list_coordinates[y][x])
        y += 1
        x -= 1

    y = yy - 1
    x = xx + 1
    while x <= 8 and y >= 0:  # добавляем элементы слева направо, снизу вверх
        diagonal_y_x.append(list_coordinates[y][x])
        y -= 1
        x += 1
    # диагональ у=-х
    y = yy - 1
    x = xx - 1
    while y >= 0 and x >= 0:  # добавляем элементы справа налево, снизу вверх
        diagonal_y_minus_x.insert(0, list_coordinates[y][x])
        y -= 1
        x -= 1

    y = yy + 1
    x = xx + 1
    while x <= 8 and y <= 8:  # добавляем элементы слева направо, сверху вниз
        diagonal_y_minus_x.append(list_coordinates[y][x])
        y += 1
        x += 1
    #print(diagonal_y_x, yy, xx)
    #print(diagonal_y_minus_x, yy, xx)
    return diagonal_y_x, diagonal_y_minus_x


def proverka_combo(yy, xx, code_colour):  # проверка на собранность комбинации из более 4 кружков по четырём направлениям
    global flag_add_balls
    count = 0  # счётчик того сколько накинуть очков после поиска всех комбинаций
    diagonal_y_x = []
    diagonal_y_minus_x = []
    # делаем 4 массива для данной клетки (строка, столбик, две диагонали)
    stroka = pole[yy]  # извлечем из матрицы столбик и строку для проверки комбинации для того поля куда поставили кружок
    stolbik = [pole[i][xx] for i in range(9)]
    diagonal_y_x_coordinates, diagonal_y_minus_x_coordinates = bild_diagonals(yy, xx) # получим координаты диагоналей для данной клетки
    for i in diagonal_y_x_coordinates:  # соберём массив значений из поля для одной диагонали
        diagonal_y_x += [pole[i[1]][i[0]]]
    for i in diagonal_y_minus_x_coordinates:  # соберём массив значений из поля для другой диагонали
        diagonal_y_minus_x += [pole[i[1]][i[0]]]
    # отправим эти массивы в функцию поиска максимальной длинны последовательности для данного цвета
    xmin, xmax = max_posl(stroka, code_colour) # вызовем функцию поиска максимально длинной последовательности для строки
    ymin, ymax = max_posl(stolbik, code_colour)  # для столбика
    y_x_min, y_x_max = max_posl(diagonal_y_x, code_colour)
    y_minus_x_min, y_minus_x_max = max_posl(diagonal_y_minus_x, code_colour)
    #print(xmin, xmax)
    #print(ymin, ymax)
    #print('d1', y_x_min, y_x_max, diagonal_y_x, code_colour)
    #print('d2', y_minus_x_min, y_minus_x_max, diagonal_y_minus_x, code_colour)
    #print('-----------------------------')
    # проверим строку
    if xmax - xmin >= 4: # если последовательность больше 5 то удалим всю её из матрицы, перекрасим поле и накинем очков
        for i in range(xmin, xmax+1):
            pole[yy][i] = 'x'
            globals()['button{}{}'.format(yy+y_shift, i)]['image'] = ''
            globals()['button{}{}'.format(yy + y_shift, i)]['width'] = 8
            globals()['button{}{}'.format(yy + y_shift, i)]['height'] = 4
        count += xmax - xmin
        flag_add_balls = False  # флагом обозначим чтобы не добавлять новых кружков на поле
    # проверим столбик
    if ymax - ymin >= 4:
        for i in range(ymin, ymax+1):
            pole[i][xx] = 'x'
            globals()['button{}{}'.format(i + y_shift, xx)]['image'] = ''
            globals()['button{}{}'.format(i + y_shift, xx)]['width'] = 8
            globals()['button{}{}'.format(i + y_shift, xx)]['height'] = 4
        count += ymax - ymin
        flag_add_balls = False
    # проверим диагональ у=х
    if y_x_max - y_x_min >= 4: # если последовательность больше 5 то удалим всю её из матрицы, перекрасим поле и накинем очков
        for i in range(y_x_min, y_x_max+1):
            pole[diagonal_y_x_coordinates[i][1]][diagonal_y_x_coordinates[i][0]] = 'x'
            globals()['button{}{}'.format(diagonal_y_x_coordinates[i][1] + y_shift, diagonal_y_x_coordinates[i][0])]['image'] = ''
            globals()['button{}{}'.format(diagonal_y_x_coordinates[i][1] + y_shift, diagonal_y_x_coordinates[i][0])]['width'] = 8
            globals()['button{}{}'.format(diagonal_y_x_coordinates[i][1] + y_shift, diagonal_y_x_coordinates[i][0])]['height'] = 4
        count += y_x_max - y_x_min
        flag_add_balls = False  # флагом обозначим чтобы не добавлять новых кружков на поле
    # проверим диагональ у=-х
    if y_minus_x_max - y_minus_x_min >= 4: # если последовательность больше 5 то удалим всю её из матрицы, перекрасим поле и накинем очков
        for i in range(y_minus_x_min, y_minus_x_max+1):
            pole[diagonal_y_minus_x_coordinates[i][1]][diagonal_y_minus_x_coordinates[i][0]] = 'x'
            globals()['button{}{}'.format(diagonal_y_minus_x_coordinates[i][1] + y_shift, diagonal_y_minus_x_coordinates[i][0])]['image'] = ''
            globals()['button{}{}'.format(diagonal_y_minus_x_coordinates[i][1] + y_shift, diagonal_y_minus_x_coordinates[i][0])]['width'] = 8
            globals()['button{}{}'.format(diagonal_y_minus_x_coordinates[i][1] + y_shift, diagonal_y_minus_x_coordinates[i][0])]['height'] = 4
        count += y_minus_x_max - y_minus_x_min
        flag_add_balls = False  # флагом обозначим чтобы не добавлять новых кружков на поле
    if count > 0:
        count += 1
    if count > 5 and count < 10:
        count = count + (count-5)*10
    elif count > 9:
        count = count + (count-9)*10 + (count-9)*100
    label_ochki['text'] += count


def button(a, b):  # обработка событий от нажатия на кнопки
    global animate_x, animate_y, indefikator_animate
    global flag_add_balls
    global c, d, flag
    global colour_choise
    if globals()['button{}{}'.format(a, b)]['image'] != '' and flag is False:  # если при нажатии кнопки она имеет кружок, то уменьшим её(выберем) и флаг выбора сделаем True
        animate_y = a  # координаты для анимации шарика в нужной кнопке. если использовать after, то ничего передавать в функцию нельзя. переменные только global
        animate_x = b
        colour_choise = int(globals()['button{}{}'.format(a, b)]['image'][7:])-1
        indefikator_animate = window.after(50, animate)
        #colour_choise = globals()['button{}{}'.format(a, b)]['bg']
        #globals()['button{}{}'.format(a, b)]['width'] = 6
        #globals()['button{}{}'.format(a, b)]['height'] = 3
        c = a
        d = b
        flag = True
    elif globals()['button{}{}'.format(a, b)]['image'] == '' and flag is True:  # если кнопка не имеет кружка, а флаг тру, то поставим туда кружок из предыдущего выбора
        possible = check_path(c-y_shift, d, a-y_shift, b)
        if possible is True:
            window.after_cancel(indefikator_animate)
            globals()['button{}{}'.format(a, b)]['image'] = list_colours[colour_choise]
            globals()['button{}{}'.format(a, b)]['width'] = 60
            globals()['button{}{}'.format(a, b)]['height'] = 65
            pole[a-y_shift][b] = colour_choise  # добавим в матрицу код цвета

            globals()['button{}{}'.format(c, d)]['width'] = 8  # предыдущую кнопку сдеаем большой и уберём кружок
            globals()['button{}{}'.format(c, d)]['height'] = 4
            globals()['button{}{}'.format(c, d)]['image'] = ''
            pole[c-y_shift][d] = 'x'  # уберём из матрицы код цвета (поставим x)
            proverka_combo(a-y_shift, b, colour_choise)
            if flag_add_balls is True:
                random_add()
                next_random_colours()
                for i in range(3):
                    globals()['label_{}'.format(i+1)]['image'] = list_colours[next_colours[i]]
            flag_add_balls = True
            flag = not flag
    elif globals()['button{}{}'.format(a, b)]['image'] != '' and flag is True:  # если решили выбрать другой кружок
        window.after_cancel(indefikator_animate)
        globals()['button{}{}'.format(c, d)]['image'] = list_colours[colour_choise]
        flag = False


def check_path(past_y, past_x, future_y, future_x):
    global pole
    pole_path = [['x' for i in range(11)] for j in range(11)] # создадим матрицу из "х" с рамкой которая не позволит алгоритму выйти за границу игрового поля
    for i in range(1, 10):  # поле внутри проинициализируем нулями
        for j in range(1, 10):
            pole_path[i][j] = 0
    for i in range(0, 9):  # пройдёмся по матрице игрового поля и заменим в поле пути нули на "х" в тех местах где стоят коды цветов (это стенки и через них пройти нельзя)
        for j in range(0, 9):
            if pole[i][j] != 'x':
                pole_path[i+1][j+1] = 'x'
    #Проверка пути. Есть ли он вообще такой...
    pole_path[past_y+1][past_x+1] = 1
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
    if pole_path[future_y + 1][future_x + 1] == 1:
        return True
    else:
        return False
#------------------------------------------------------------------
    #for i in range(11):  # печать
        #for j in range(11):
            #pole_path[i][j] = str(pole_path[i][j])
    #for i in range(11):
        #print(' '.join(pole_path[i]))
    #print('------------------------------------------')
#------------------------------------------------------------------


def reset():  # начать игру заново
    global pole
    for i in range(3, 12):
        for j in range(9):
            globals()['button{}{}'.format(i, j)]['image']=''
            globals()['button{}{}'.format(i, j)]['width'] = 8
            globals()['button{}{}'.format(i, j)]['height'] = 4
    label_ochki['text'] = 0
    pole = [['x' for i in range(9)] for j in range(9)]
    random_add()
    next_random_colours()
    for i in range(3):
        globals()['label_{}'.format(i + 1)]['image'] = list_colours[next_colours[i]]


def animate():
    global level, flag_animate, animate_y, animate_x, indefikator_animate, colour_choise
    globals()['button{}{}'.format(animate_y, animate_x)]['image'] = list_colours_move[level][colour_choise]
    level += 1
    if level == 24:
        level = 0
    indefikator_animate = window.after(25, animate)


window = tkinter.Tk()
window.title('Lines. версия от Alex_chel_man')


list_colours = [tkinter.PhotoImage(file=i) for i in list_file_static]  # статические объекты для программы кружков
list_colours_move = [[tkinter.PhotoImage(file=i, format='gif - {}'.format(j))for i in list_file_move] for j in range(24)]  # сдоровенный массив из целой кучи слоёв прыгающих кружков
next_random_colours()

label_chet = tkinter.Label(window, text='Счёт:', font='Arial 14')
label_ochki = tkinter.Label(window, text=0, font='Arial 14')
label_1 = tkinter.Label(window, width=60, height=65, relief='ridge')
label_2 = tkinter.Label(window, width=60, height=65, relief='ridge')
label_3 = tkinter.Label(window, width=60, height=65, relief='ridge')

label_chet.grid(row=0, column=3)
label_ochki.grid(row=0, column=4)
label_1.grid(row=2, column=3)
label_2.grid(row=2, column=4)
label_3.grid(row=2, column=5)

for i in range(3, 12):
    for j in range(9):
        globals()['button{}{}'.format(i, j)] = tkinter.Button(width=8, height=4, command=lambda a=i, b=j: button(a, b), bg='snow1')
        globals()['button{}{}'.format(i, j)].grid(row=i, column=j)

button_reset = tkinter.Button(window, text='Начать\nзаново', command=reset)
button_reset.grid(row=2, column=8)

random_add()
# for i in range(9): print(pole[i])
next_random_colours()
for i in range(3):
    globals()['label_{}'.format(i + 1)]['image'] = list_colours[next_colours[i]]


window.geometry('595x740')
window.mainloop()
