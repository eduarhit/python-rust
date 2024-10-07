import multiprocessing
# import time
import calculations_rs
#
#
# def worker(numbers, start, end, result):
#     """A worker function to calculate squares of numbers."""
#     for i in range(start, end):
#         result[i] = numbers[i] * numbers[i]
#
#
# def main(core_count):
#     numbers = range(900000)  # A larger range for a more evident effect of multiprocessing
#     result = multiprocessing.Array('i', len(numbers))
#     segment = len(numbers) // core_count
#     processes = []
#
#     for i in range(core_count):
#         start = i * segment
#         if i == core_count - 1:
#             end = len(numbers)  # Ensure the last segment goes up to the end
#         else:
#             end = start + segment
#         # Creating a process for each segment
#         p = multiprocessing.Process(target=worker, args=(numbers, start, end, result))
#         processes.append(p)
#         p.start()
#
#     for p in processes:
#         p.join()
#
#     return result
#
#

import time
import threading



def calc_square(numbers):
    result = []
    for n in numbers:
        result.append(n**2)
        # time.sleep(0.001)
    return result

def calc_cube(numbers):
    result = []
    for n in numbers:
        result.append(n*3)
        # time.sleep(0.001)
    return result


if __name__ == '__main__':
    core_count = 8
    iterations = int(4096)
    numbers = list(range(1, 10000))

    # # Single threading
    # start = time.time()
    # for _ in range(iterations):
    #     calc_square(numbers)
    #     calc_cube(numbers)
    # end = time.time()
    # print(f'Execution Time Single threadPython: {end - start} seconds')

    # Using multithreading library
    start = time.time()
    threads = []
    for _ in range(iterations):
        threads.append(threading.Thread(target=calc_square, args=(numbers,)))
        threads.append(threading.Thread(target=calc_cube, args=(numbers,)))

        threads[-2].start()
        threads[-1].start()

    for thr in threads:
        thr.join()
    end = time.time()
    print(f'Execution Time Multi thread Python: {end - start} seconds')

    # # Using multiprocessing library
    # start = time.time()
    # processes = []
    # for _ in range(iterations):
    #     processes.append(multiprocessing.Process(target=calc_square, args=(numbers,)))
    #     processes.append(multiprocessing.Process(target=calc_cube, args=(numbers,)))
    #     processes[-2].start()
    #     processes[-1].start()
    #
    # for p in processes:
    #     p.join()
    # end = time.time()
    # print(f'Execution Time Multi Process Python: {end - start} seconds')

    # Using rust
    calculations_rs.multiply()

