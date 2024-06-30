import time
import asyncio


async def some_io_bound_task():
    print("Emulate of HTTP request")
    await asyncio.sleep(4)


async def main():
    tasks = [some_io_bound_task() for _ in range(3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Total execution time: {time.time() - start}")
