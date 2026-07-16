import asyncio

counter = 0
lock = asyncio.Lock()


async def unsafe_increment():
    global counter

    tmp = counter          # прочитали общее состояние
    await asyncio.sleep(0.1) # здесь отдали управление event loop
    counter = tmp + 1      # записали устаревшее значение


async def safe_increment():
    global counter

    async with lock:
        tmp = counter
        await asyncio.sleep(0.1)
        counter = tmp + 1


async def main():
    global counter

    # Гонка
    counter = 0
    await asyncio.gather(*(unsafe_increment() for _ in range(1000)))
    print("Без lock:", counter)

    # Синхронизация
    counter = 0
    await asyncio.gather(*(safe_increment() for _ in range(1000)))
    print("С lock:", counter)


asyncio.run(main())