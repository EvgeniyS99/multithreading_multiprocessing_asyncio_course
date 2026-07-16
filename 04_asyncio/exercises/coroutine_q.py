async def foo():
    print("start")
    x = await bar()
    print("after await", x)
    return 42

async def bar():
    print("bar start")
    return 10

coro = foo()

coro.send(None)
coro.send(None)