import asyncio


async def some_task():
    try:
        while True:
            print("Running...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task was cancelled")
        raise
    finally:
        print("Resources are cleaned up")


async def main():
    task = asyncio.create_task(some_task())
    await asyncio.sleep(5)  # Позволим задаче поработать некоторое время
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Main: Task was cancelled")

asyncio.run(main())
