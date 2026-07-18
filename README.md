# Python Concurrency Course

Course materials covering operating-system foundations, Python concurrency,
parallel processing, `asyncio`, and asynchronous web applications.

## Course structure

| Lesson | Topic | Presentation | Supporting materials |
| --- | --- | --- | --- |
| 1 | OS and CPU recap | [Presentation](01_os_cpu_recap/01_os_cpu_recap.pdf) | Process context example and notebook |
| 2 | Multithreading | [Presentation](02_multithreading/02_multithreading.pdf) | Threading notebook and examples |
| 3 | Multiprocessing | [Presentation](03_multiprocessing/03_multiprocessing.pdf) | Process, IPC, pool, and GPU examples |
| 4 | Async and `asyncio` | [Presentation](04_asyncio/04_asyncio.pdf) | Coroutine notebook, examples, and quiz |
| 5 | Networks, WSGI, ASGI, and FastAPI | [Presentation](05_async_web/05_async_web.pdf) | Protocol and web-service examples |

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

## Author

Designed and authored by [EvgeniyS99](https://github.com/EvgeniyS99).