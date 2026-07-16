async def app(scope, receive, send):
    # В отличие от HTTP, websocket app вызывается один раз на соединение
    assert scope["type"] == "websocket"

    await send({"type": "websocket.accept"})

    while True:
        message = await receive()
        if message["type"] == "websocket.receive":
            text = message.get("text", "")
            await send({"type": "websocket.send", "text": f"{text}, пидор"})
        elif message["type"] == "websocket.disconnect":
            break

# wscat -c ws://127.0.0.1:8000