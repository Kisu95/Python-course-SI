import numpy as np
import time

random_numbers = np.random.randint(1, 10001, 100)
lenth_of_array = len(random_numbers)


def first_method(numbers_tuple):
    clock_start = time.perf_counter()
    sorted_by_function = sorted(numbers_tuple,
                                key=lambda tup: tup[1], reverse=True)
    clock_stop = time.perf_counter()
    print(
        f"Sorting the array by function took {clock_stop - clock_start:0.10f} seconds")
    print(f"Sorted indexes: {indexes(sorted_by_function)}")


def second_method(numbers_tuple):
    lst = len(numbers_tuple)
    clock_start = time.perf_counter()
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if (numbers_tuple[j][1] < numbers_tuple[j + 1][1]):
                temp = numbers_tuple[j]
                numbers_tuple[j] = numbers_tuple[j + 1]
                numbers_tuple[j + 1] = temp
    clock_stop = time.perf_counter()
    print(
        f"Sorting the array by function took {clock_stop - clock_start:0.10f} seconds")
    print(f"Sorted indexes: {indexes(numbers_tuple)}")


def three_larger_numbers_indexes(list_of_numbers, threshold_value):
    numbers_with_indexes = []
    for count, element in enumerate(list_of_numbers):
        if len(numbers_with_indexes) < 3 and int(element) > threshold_value:
            numbers_with_indexes.append(tuple((count, element)))
    first_method(numbers_with_indexes.copy())
    second_method(numbers_with_indexes.copy())


def indexes(tuple_list):
    indexes = []
    for element in tuple_list:
        indexes.append(element[0])
    return indexes


three_larger_numbers_indexes(
    [9, 1, 1, 1, 0, 0, 0, 8, 10, 11, 14, 2132323, 24234524], 2)
