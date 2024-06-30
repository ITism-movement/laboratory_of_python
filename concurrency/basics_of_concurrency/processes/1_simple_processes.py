import time
from multiprocessing import Process
import os


def some_cpu_bound_task(n: int) -> int:
    print(f"Process with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


if __name__ == "__main__":
    start = time.time()
    n = 1_000_000_000
    process = Process(target=some_cpu_bound_task, args=(n,))
    print(f"This is the process {os.getpid()}")
    process.start()
    process.join()
    print(f"Total execution time: {time.time() - start}")
