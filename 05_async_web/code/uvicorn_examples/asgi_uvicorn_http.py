import asyncio

async def app(scope, receive, send):
    # В HTTP app вызывается на каждый request
    assert scope["type"] == "http"

    # дочитываем request body
    body = bytearray()
    while True:
        event = await receive()
        assert event["type"] == "http.request"
        body.extend(event.get("body", b""))
        if not event.get("more_body", False):
            break

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain; charset=utf-8")],
    })

    # стримим response чанками
    for i in range(5):
        await send({
            "type": "http.response.body",
            "body": f"chunk {i}, request_size={len(body)}\n".encode(),
            "more_body": True,
        })
        await asyncio.sleep(1)

    await send({
        "type": "http.response.body",
        "body": b"done\n",
        "more_body": False,
    })


# uvicorn asgi_uvicorn_http:app --host 127.0.0.1 --port 8999
# curl -X POST http://127.0.0.1:8999/ -d 'hello Zheka'