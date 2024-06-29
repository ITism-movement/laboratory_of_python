from threading import Thread
import os


def some_cpu_bound_task(n: int) -> int:
    print(f"Thread with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


if __name__ == "__main__":
    n = 1_000_000_000
    thread = Thread(target=some_cpu_bound_task, args=(n,))
    print(f"This is the process {os.getpid()}")
    thread.start()
