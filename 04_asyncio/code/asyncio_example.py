import asyncio
import socket


async def socket_demo(loop: asyncio.AbstractEventLoop) -> bytes:
    print("\n--- socket_demo ---")

    # Локальная пара связанных сокетов: один пишет, другой читает.
    rsock, wsock = socket.socketpair()

    # Для loop.sock_recv сокет должен быть неблокирующим.
    rsock.setblocking(False)
    wsock.setblocking(False)

    try:
        # Через 0.2 сек "как будто сеть прислала данные"
        loop.call_later(10, wsock.send, b"hello from socket")

        print("Ждём данные из неблокирующего сокета...")
        data = await loop.sock_recv(rsock, 1024)
        print("Получили из сокета:", data)
        return data
    finally:
        rsock.close()
        wsock.close()


async def future_demo(loop: asyncio.AbstractEventLoop) -> str:
    print("\n--- future_demo ---")

    # Правильный способ создать Future, привязанный к текущему loop
    fut = loop.create_future()

    def on_done(done_fut: asyncio.Future) -> None:
        print("done callback сработал; result =", done_fut.result())

    fut.add_done_callback(on_done)

    # Через 0.3 сек кто-то "снаружи" завершит future
    loop.call_later(0.3, fut.set_result, "manual future resolved")

    print("Ждём ручной Future...")
    result = await fut
    print("await fut вернул:", result)
    return result


async def main(mode) -> None:
    # asyncio.run(main()) создаёт и запускает top-level event loop
    loop = asyncio.get_running_loop()
    print("Текущий loop:", loop)

    if mode == 'future':
        future_result = await future_demo(loop)
        print("\nИтог:")
        print("future_result =", future_result)
    elif mode == 'socket':
        socket_result = await socket_demo(loop)
        print("\nИтог:")
        print("socket_result =", socket_result)
    elif mode == 'all':
        socket_result = await socket_demo(loop)
        future_result = await future_demo(loop)


if __name__ == "__main__":
    mode = 'all'
    asyncio.run(main(mode=mode))