from multiprocessing import Pool
import os
import requests
import time


def some_io_bound_task(n):
    print(f"Process with id {os.getpid()} has been started!")
    response = requests.get("https://example.com")
    time.sleep(n)
    return response.status_code


if __name__ == "__main__":
    n = 1
    num_of_processes = 3

    # Run with Pool
    pool = Pool(processes=num_of_processes)
    results = pool.map(some_io_bound_task, [n] * num_of_processes)
    print(results)
