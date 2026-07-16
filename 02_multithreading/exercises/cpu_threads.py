from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import time

import numpy as np
from numba import njit


DIR = Path("./files")
NUM_FILES = 20
FILE_SIZE_MB = 10
MAX_WORKERS = 2
N_REPS = 8
CPU_LIST_SIZE = 1000


def prepare_files() -> list[Path]:
    DIR.mkdir(exist_ok=True)
    paths = []
    expected_size = FILE_SIZE_MB * 1024 * 1024

    for i in range(NUM_FILES):
        path = DIR / f"file_{i}.bin"
        paths.append(path)

        if path.exists() and path.stat().st_size == expected_size:
            continue

        print(f"Создаю {path}...")
        chunk = os.urandom(1024 * 1024)

        with open(path, "wb") as f:
            for _ in range(FILE_SIZE_MB):
                f.write(chunk)

    return paths


def small_cpu_work_python(arr: np.ndarray) -> int:
    total = 0
    n = arr.shape[0]

    for i in range(n):
        for j in range(n):
            arr[i] += (j & 1)
            total += arr[i]

    return total


@njit(nogil=True)
def small_cpu_work_numba(arr):
    total = 0
    n = arr.shape[0]

    for i in range(n):
        for j in range(n):
            arr[i] += (j & 1 )
            total += arr[i]

    return total


def read_file_python(path: Path) -> int:
    arr = np.zeros(CPU_LIST_SIZE, dtype=np.int64)
    _ = small_cpu_work_python(arr)

    with open(path, "rb") as f:
        data = f.read()
    return len(data)


def read_file_numba(path: Path) -> int:
    arr = np.zeros(CPU_LIST_SIZE, dtype=np.int64)
    _ = small_cpu_work_numba(arr)

    with open(path, "rb") as f:
        data = f.read()
    return len(data)


def bench_sync(paths: list[Path], reader) -> float:
    start = time.perf_counter()
    total = 0

    for path in paths:
        total += reader(path)

    elapsed = time.perf_counter() - start
    print(f"[sync] total bytes read = {total}")
    return elapsed


def bench_threads_submit(paths: list[Path], max_workers: int, reader) -> float:
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(reader, path) for path in paths]

        total = 0
        for future in futures:
            total += future.result()

    elapsed = time.perf_counter() - start
    print(f"[threads-submit] total bytes read = {total}")
    return elapsed


def run_case(title: str, paths: list[Path], reader) -> None:
    print(f"\n=== {title} ===")

    for _ in range(N_REPS):
        sync_time = bench_sync(paths, reader)
        thread_time = bench_threads_submit(paths, MAX_WORKERS, reader)

        print(f"sync:    {sync_time:.3f} sec")
        print(f"threads: {thread_time:.3f} sec")
        print(f"speedup: {sync_time / thread_time:.2f}x")
        print()


def main() -> None:
    print("all logical CPUs:", os.cpu_count())
    print("affinity before:", os.sched_getaffinity(0))
    #os.sched_setaffinity(0, {0})
    print("affinity after:", os.sched_getaffinity(0))
    paths = prepare_files()

    warmup = np.zeros(CPU_LIST_SIZE, dtype=np.int64)
    _ = small_cpu_work_numba(warmup)

    run_case("Python CPU work O(N^2) + I/O", paths, read_file_python)
    run_case("Numba CPU work O(N^2) + I/O", paths, read_file_numba)


if __name__ == "__main__":
    main()