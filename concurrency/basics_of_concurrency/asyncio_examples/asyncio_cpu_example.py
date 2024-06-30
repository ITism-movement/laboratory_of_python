import os
import time
import asyncio


async def some_cpu_bound_task(n: int) -> int:
    print(f"Process with id {os.getpid()} has been started!")
    return sum([1 for _ in range(n)])


async def main(n):
    await asyncio.gather(*[some_cpu_bound_task(n)])


if __name__ == "__main__":
    start = time.time()
    n = 1_000_000_000
    asyncio.run(main(n))
    num_of_processes = 3
    print(f"Total execution time: {time.time() - start}")
