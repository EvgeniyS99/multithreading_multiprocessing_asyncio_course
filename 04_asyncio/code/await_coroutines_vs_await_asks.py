import asyncio
import time

async def worker(name):
    print(name, "start")
    await asyncio.sleep(1)
    print(name, "done")

async def sequential_coroutines():
    # Эти корутины живут внутри главного task
    cor1 = worker("A")
    cor2 = worker("B")
    cor3 = worker("C")

    start = time.perf_counter()
    await cor1 # Здесь мы начинаем выполнять корутину В РАМКАХ ТЕКУЩЕЙ TASK до первого await - потом event loop может переключиться на другие tasks, если они есть
               # Если их нет, то мы будем дожиидаться, пока вся корутина не выполнится
    await cor2
    await cor3
    end = time.perf_counter()
    return end - start

async def concurrent_tasks():
    task1 = asyncio.create_task(worker("A")) # This creates a Task_1 object and schedules its execution via the event loop.
    task2 = asyncio.create_task(worker("B")) # This creates a Task_2 object and schedules its execution via the event loop.
    task3 = asyncio.create_task(worker("C")) # This creates a Task_3 object and schedules its execution via the event loop.
    await asyncio.sleep(5)
    start = time.perf_counter()
    # await task1 # Здесь мы передаем контроль event loop и он может начать выполнять tasks конкуретно
    # await task2 # Этот await уже ждет завершения task2
    # await task3 # Этот await ждет завершения task3
    end = time.perf_counter()
    return end - start

async def main():
    # print("=== Последовательные await на корутинах ===")
    # t1 = await sequential_coroutines()
    # print(f"Время: {t1:.3f} сек\n")

    print("=== create_task + await ===")
    t2 = await concurrent_tasks()
    print(f"Время: {t2:.3f} сек\n")

asyncio.run(main())