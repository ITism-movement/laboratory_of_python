from threading import Thread
import os
import time


def some_cpu_bound_task(n: int) -> int:
    print(f"Thread with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


if __name__ == "__main__":
    start = time.time()
    n = 100_000_000

    # Run 3 processes simultaneously
    threads_list = []
    for _ in range(3):
        thread = Thread(target=some_cpu_bound_task, args=(n, ))
        threads_list.append(thread)
        thread.start()
    for thread in threads_list:
        thread.join()
    print(f"Total execution time: {time.time() - start}")
