import asyncio

async def worker(name):
    print(name, "start")
    await asyncio.sleep(1)
    print(name, "done")

async def main():
    asyncio.create_task(worker("A"))
    asyncio.create_task(worker("B"))
    asyncio.create_task(worker("C"))

asyncio.run(main())