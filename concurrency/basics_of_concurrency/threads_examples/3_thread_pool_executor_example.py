from concurrent.futures import ThreadPoolExecutor
import os
import time
import requests


def some_cpu_bound_task(n: int) -> int:
    print(f"Thread with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


def some_io_bound_task(n):
    print(f"Process with id {os.getpid()} has been started!")
    response = requests.get("https://example.com")
    time.sleep(n)
    return response.status_code


if __name__ == "__main__":
    start = time.time()
    n = 1

    # Run 3 threads simultaneously
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(some_io_bound_task, [n] * 3))
    print(f"Total execution time: {time.time() - start}")
