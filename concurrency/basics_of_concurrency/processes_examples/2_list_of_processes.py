import time
from multiprocessing import Process
import os


def some_cpu_bound_task(n: int) -> int:
    print(f"Process with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


if __name__ == "__main__":
    start = time.time()
    n = 100_000_000

    # Run 3 processes simultaneously
    processes_list = []
    for _ in range(3):
        process = Process(target=some_cpu_bound_task, args=(n, ))
        processes_list.append(process)
        process.start()
    for process in processes_list:
        process.join()
    print(f"Total execution time: {time.time() - start}")
