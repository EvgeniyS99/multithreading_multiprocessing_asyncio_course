# Lesson 5: Networks, WSGI, ASGI, and FastAPI

This lesson connects TCP, HTTP, and WebSocket fundamentals to Python web-server
interfaces. It covers WSGI, ASGI, Uvicorn, FastAPI, application lifespan, and a
production-style asynchronous ML inference service.

## Materials

- [Presentation](presentation.pptx)
- [Async web notebook](notebooks/async_web.ipynb)
- [`custom_wsgi.py`](code/custom_wsgi.py) — educational WSGI server
- Raw ASGI examples in `code/uvicorn_examples/`
- FastAPI HTTP and WebSocket examples in `code/dummy_app/`
- `code/lecture_fragments.txt` — pseudocode fragments used while presenting the underlying
  socket, event-loop, and WSGI concepts

Example commands:

```bash
uvicorn code.uvicorn_examples.asgi_uvicorn_http:app --port 8999
python code/dummy_app/run_app.py
```
