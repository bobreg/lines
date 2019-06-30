a = [int(i) for i in input().split()]
a.append('x')
# a = [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0]
print(a)
xmin = -1
xmax = -1
max_len_one_old = 0
try:
    min_one_index = a.index(1)
    i = min_one_index + 1
    len_one = 1
    max_len_one = 1
    while min_one_index < len(a) and i < len(a):
        if a[i] == a[min_one_index] and a[min_one_index] == 1:
            i += 1
            len_one += 1
        else:
            max_len_one = max(max_len_one, len_one)
            if max_len_one > max_len_one_old:
                xmin = min_one_index
                xmax = i - 1
                max_len_one_old = max_len_one
            min_one_index = i
            i = min_one_index + 1
            len_one = 1
    max_len_one = max(max_len_one, len_one)
    print(max_len_one, xmin, xmax)
except ValueError:
    print(0, xmin, xmax)
