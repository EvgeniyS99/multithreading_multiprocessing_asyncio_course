import asyncio

async def worker(name):
    print(name, "start")
    await asyncio.sleep(1) # some non blocking i/o operation
    print(name, "done")

async def main():
    # task1 = asyncio.create_task(worker("A"))
    # task2 = asyncio.create_task(worker("B"))
    # task3 = asyncio.create_task(worker("C"))

    # await task1
    # await task2
    # await task3
    
    await asyncio.gather(
        worker("A"),
        worker("B"),
        worker("C"),
    )

asyncio.run(main())