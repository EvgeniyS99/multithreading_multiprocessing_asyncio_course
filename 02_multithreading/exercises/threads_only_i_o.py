from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import time


DIR = Path("./files")
NUM_FILES = 50
FILE_SIZE_MB = 10
MAX_WORKERS = 2
N_REPS = 8


def prepare_files() -> list[Path]:
    DIR.mkdir(exist_ok=True)
    paths = []

    for i in range(NUM_FILES):
        path = DIR / f"file_{i}.bin"
        paths.append(path)

        if path.exists() and path.stat().st_size >= FILE_SIZE_MB * 1024 * 1024:
            continue

        print(f"Создаю {path}...")
        chunk = os.urandom(1024 * 1024)  # 1 MB

        with open(path, "wb") as f:
            for _ in range(FILE_SIZE_MB):
                f.write(chunk)

    return paths


def read_file(path: Path) -> int:
    with open(path, "rb") as f:
        data = f.read()
    return len(data)


def bench_sync(paths: list[Path]) -> float:
    start = time.perf_counter()
    total = 0

    for path in paths:
        total += read_file(path)

    elapsed = time.perf_counter() - start
    print(f"[sync] total bytes read = {total}")
    return elapsed


def bench_threads_submit(paths: list[Path], max_workers: int) -> float:
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for path in paths:
            future = executor.submit(read_file, path)
            futures.append(future)

        total = 0
        for future in futures:
            total += future.result()

    elapsed = time.perf_counter() - start
    print(f"[threads-submit] total bytes read = {total}")
    return elapsed


def main() -> None:
    print("all logical CPUs:", os.cpu_count())
    print("affinity before:", os.sched_getaffinity(0))
    print("available by affinity:", len(os.sched_getaffinity(0)))
    os.sched_setaffinity(0, {0})
    print("affinity after:", os.sched_getaffinity(0))

    for _ in (range(N_REPS)):
        paths = prepare_files()
    
        sync_time = bench_sync(paths)
        thread_time = bench_threads_submit(paths, MAX_WORKERS)
    
        print()
        print(f"sync:    {sync_time:.3f} sec")
        print(f"threads: {thread_time:.3f} sec")
        print(f"speedup: {sync_time / thread_time:.2f}x")


if __name__ == "__main__":
    main()