import asyncio
import socket

async def child(rsock):
    loop = asyncio.get_running_loop()
    data = await loop.sock_recv(rsock, 1024)
    return data

async def main(rsock):
    x = await child(rsock)
    return x + b" + processed"

async def demo():
    loop = asyncio.get_running_loop()

    rsock, wsock = socket.socketpair()
    rsock.setblocking(False)
    wsock.setblocking(False)

    loop.call_later(0.1, wsock.send, b"hello")

    try:
        result = await main(rsock)
        print(result)
    finally:
        rsock.close()
        wsock.close()

asyncio.run(demo())


# 1. создается event loop, соаздется корутина demo(), она оборачивается в Task, loop запускается (loop.run_until_complete())
# 2. task отправляет в очередь, у нее вызывается task._step(), внутри которой делается coro.send(None) - запуск demo с начала
# 3. Внутри demo берется event_loop, создаются два сокета и переводятся в неблокирующий режим
# 4. demo дошел до await main(rsock) -> вызвался child(rsock) - создал корутину child -> таска вызвала child_coro.send(None) - она завелась
# 5. await loop.sock_recv(rsock, 1024) - асинхронно ожидаем сокет -- под капотом создается объект Future, loop регистрирует fd сокета на чтение -> как только он получит данные, вызыветеся специальный callback on_readable(), который поместит в future резлуьтат из сокета -> таким образом мы свалились до Future и прощошел await future -> fut.add_done_callback(task_demo._wakeup)
# 6. event loop с помощью селектора проверяет, попали ли что-то в очередь готовых тасок
# 7. как только попало, ему selector дает об этом знать  и loop начинается вызывать колбеки, в том числе вызывает колбек _wakeup, который вызывает _step(b"hello") (все равно что send(b"hello") -> эта штука прилетает в x -> main возвращает в демо b"hello + processed"