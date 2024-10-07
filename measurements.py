import multiprocessing
import time
import calculations_rs


def worker(numbers, start, end, result):
    """A worker function to calculate squares of numbers."""
    for i in range(start, end):
        result[i] = numbers[i] * numbers[i]


def main(core_count):
    numbers = range(900000)  # A larger range for a more evident effect of multiprocessing
    result = multiprocessing.Array('i', len(numbers))
    segment = len(numbers) // core_count
    processes = []

    for i in range(core_count):
        start = i * segment
        if i == core_count - 1:
            end = len(numbers)  # Ensure the last segment goes up to the end
        else:
            end = start + segment
        # Creating a process for each segment
        p = multiprocessing.Process(target=worker, args=(numbers, start, end, result))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return result


if __name__ == '__main__':
    print(f"{multiprocessing.cpu_count()} cores available")
    for core_count in [1, 2, 4, 8, 16, 32]:
        start = time.time()
        print(f"Using {core_count} cores:")
        result = main(core_count)
        print(f"Time taken in python: {time.time() - start:.2f} seconds")

    calculations_rs.multiply()
