import asyncio


async def fail_task():
    return 1 / 0


async def success_task():
    return "success"


async def main():
    results = await asyncio.gather(fail_task(), success_task(), return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            print(f"Caught exception: {result}")
        else:
            print(f"Task result: {result}")

asyncio.run(main())
