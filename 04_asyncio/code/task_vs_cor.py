import asyncio

async def coro_a():
    print('start coro_a')
    # await asyncio.sleep(1)
    print("I am coro_a(). Hi!")

async def coro_b():
    print('start coro_b')
    print("I am coro_b(). I sure hope no one holds the event loop...")

async def main():
    task_b = asyncio.create_task(coro_b())
    num_repeats = 3
    for _ in range(num_repeats):
        task_a = asyncio.create_task(coro_a())
        #await coro_a()'
        await task_a

    await task_b

asyncio.run(main())
