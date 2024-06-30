from multiprocessing import Pool
import os
import time


def some_cpu_bound_task(n: int) -> int:
    print(f"Process with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


if __name__ == "__main__":
    start = time.time()
    n = 1_000_000_000
    num_of_processes = 3

    # Run with Pool
    pool = Pool(processes=3)
    results = pool.map(some_cpu_bound_task, [n] * num_of_processes)
    print(results)
    print(f"Total execution time: {time.time() - start}")
