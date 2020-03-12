import numpy as np
import time

random_numbers = np.random.randint(1, 10001, 100)
lenth_of_array = len(random_numbers)


def bubbleSort(array_of_numbers, lenth_of_array):
    array_of_numbers = array_of_numbers.copy()
    clock_start = time.perf_counter()
    print(f"Unsorted array: {array_of_numbers}")

    for i in range(lenth_of_array):
        for j in range(0, lenth_of_array - i-1):
            if array_of_numbers[j] > array_of_numbers[j+1]:
                array_of_numbers[j], array_of_numbers[j +
                                                      1] = array_of_numbers[j+1], array_of_numbers[j]
    print(f"Sorted array: {array_of_numbers}")
    clock_stop = time.perf_counter()
    print(f"Sorting the array took {clock_stop - clock_start:0.4f} seconds")


def quickSort(array_of_numbers):
    if len(array_of_numbers) <= 1:
        return array_of_numbers
    pivot = array_of_numbers[len(array_of_numbers) // 2]
    left = [x for x in array_of_numbers if x < pivot]
    middle = [x for x in array_of_numbers if x == pivot]
    right = [x for x in array_of_numbers if x > pivot]
    return quickSort(left) + middle + quickSort(right)


def printQuickSort(array_of_numbers):
    array_of_numbers = array_of_numbers.copy()
    clock_start = time.perf_counter()
    print(f"Unsorted array: {array_of_numbers}")
    print(f"Sorted array: {quickSort(array_of_numbers)}")
    clock_stop = time.perf_counter()
    print(f"Sorting the array took {clock_stop - clock_start:0.4f} seconds")


print(f"--------------boobleSort-----------------")
bubbleSort(random_numbers, lenth_of_array)
print(f"----------------QuickSort-------------------")
printQuickSort(random_numbers)
print(f"-------------------------------------------------")
