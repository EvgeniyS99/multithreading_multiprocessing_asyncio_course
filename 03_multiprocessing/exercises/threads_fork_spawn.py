import multiprocessing
import os
import threading
import time


def child_fork(lock):
    print("fork child started", flush=True)
    print("trying to acquire the inherited lock", flush=True)

    # Intentional deadlock: the child inherited the locked state, but the
    # parent thread that owns this threading.Lock does not exist in the child.
    lock.acquire()

    print("lock acquired", flush=True)
    lock.release()
    os._exit(0)


def child_spawn(lock):
    print("spawn child started", flush=True)
    print("waiting for the shared multiprocessing lock", flush=True)
    lock.acquire()
    print("shared lock acquired", flush=True)
    lock.release()


def demo_fork():
    """Demonstrate a deadlock caused by forking a multithreaded process."""
    lock = threading.Lock()

    def holder():
        print("holder thread started", flush=True)
        lock.acquire()
        print("threading.Lock acquired by holder", flush=True)
        time.sleep(5)
        lock.release()
        print("threading.Lock released in the parent", flush=True)

    def starter():
        print("forking thread started", flush=True)
        time.sleep(1)

        pid = os.fork()

        if pid == 0:
            child_fork(lock)
        else:
            print("parent is waiting for the fork child", flush=True)
            os.waitpid(pid, 0)

        print("parent and child completed", flush=True)

    print("Starting the intentional fork deadlock demo", flush=True)
    t1 = threading.Thread(target=holder)
    t2 = threading.Thread(target=starter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def demo_spawn():
    """Show a process-shared lock working correctly with spawn."""
    ctx = multiprocessing.get_context("spawn")
    lock = ctx.Lock()

    def holder():
        print("holder thread started", flush=True)
        lock.acquire()
        print("multiprocessing.Lock acquired by holder", flush=True)
        time.sleep(5)
        lock.release()
        print("multiprocessing.Lock released by holder", flush=True)

    def starter():
        print("spawn starter thread started", flush=True)
        time.sleep(1)

        p = ctx.Process(target=child_spawn, args=(lock,))
        p.start()
        p.join()

    print("Starting the spawn demo", flush=True)
    t1 = threading.Thread(target=holder)
    t2 = threading.Thread(target=starter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    # demo_fork() intentionally hangs. Run it explicitly when discussing why
    # fork is unsafe after other threads have started.
    demo_spawn()
