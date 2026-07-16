import os
import threading


def main() -> None:
    print("process id:", os.getpid())
    print("parent process id:", os.getppid())
    print("logical CPUs:", os.cpu_count())
    print("thread:", threading.current_thread().name)
    print("native thread id:", threading.get_native_id())

    if hasattr(os, "sched_getaffinity"):
        print("CPU affinity:", sorted(os.sched_getaffinity(0)))


if __name__ == "__main__":
    main()
