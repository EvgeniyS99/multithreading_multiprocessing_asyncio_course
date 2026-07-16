import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


def blocking_task():
    print("start blocking task")
    time.sleep(10)
    print("end blocking task")
    return 1


async def ticker():
    for i in range(5):
        print("tick", i)
        await asyncio.sleep(0.5)


async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(max_workers=1) as executor:
        ticker_task = asyncio.create_task(ticker())

        result = await loop.run_in_executor(executor, blocking_task)

        await ticker_task
        print("result:", result)


asyncio.run(main())