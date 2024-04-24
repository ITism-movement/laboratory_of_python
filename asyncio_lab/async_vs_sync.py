import time
import asyncio


def send_request(id_: int):
    print(f"Func {id_} has been executed!")
    time.sleep(1)
    print(f"Func {id_} has been completed!")


# start = time.time()
# for i in range(300):
#     send_request(i)
# print(time.time() - start)


async def send_request_async(id_: int):
    print(f"Func {id_} has been executed!")
    await asyncio.sleep(1)
    print(f"Func {id_} has been completed!")


async def main():
    start = time.time()
    l = [asyncio.create_task(send_request_async(1)) for _ in range(1000)]
    await asyncio.gather(*l[:3])
    print(time.time() - start)


asyncio.run(main())
