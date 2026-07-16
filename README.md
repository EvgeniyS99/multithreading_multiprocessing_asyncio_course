# Python Concurrency and Async Services

Course materials covering operating-system foundations, Python concurrency,
parallel processing, `asyncio`, and asynchronous web applications.

## Course structure

| Lesson | Topic | Presentation | Supporting materials |
| --- | --- | --- | --- |
| 1 | OS and CPU recap | [`01_os_cpu_recap/presentation.pptx`](01_os_cpu_recap/presentation.pptx) | Process context example and notebook |
| 2 | Multithreading | [`02_multithreading/presentation.pptx`](02_multithreading/presentation.pptx) | Threading notebook, examples, and quiz |
| 3 | Multiprocessing | [`03_multiprocessing/presentation.pptx`](03_multiprocessing/presentation.pptx) | Process, IPC, pool, and GPU examples |
| 4 | Async and `asyncio` | [`04_asyncio/presentation.pptx`](04_asyncio/presentation.pptx) | Coroutine notebook, examples, and quiz |
| 5 | Networks, WSGI, ASGI, and FastAPI | [`05_async_web/presentation.pptx`](05_async_web/presentation.pptx) | Protocol and web-service examples |

Each lesson is self-contained and has a README describing its presentation,
notebook, runnable examples, and exercises.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Most concurrency examples use only the Python standard library. Some benchmark,
computer-vision, and web examples require the optional packages listed in
`requirements.txt`.

## Presentation sources

The presentations were split from `MPS_MTHR.pptx` and `async.pptx` without
editing slide content. Quiz slides retain their original theme in companion
`quiz.pptx` files when they accompany a lecture based on the other source deck.
