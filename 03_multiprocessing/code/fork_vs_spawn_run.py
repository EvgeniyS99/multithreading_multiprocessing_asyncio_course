import os
from multiprocessing import get_context

print(f"TOP-LEVEL import, pid={os.getpid()}")

def worker():
    print(f"worker() started, pid={os.getpid()}")

def demo_spawn():
    print(f"[spawn] parent before start, pid={os.getpid()}")
    ctx = get_context("spawn")
    p = ctx.Process(target=worker) # создаем дочерний процесс
    p.start()
    p.join()
    print(f"[spawn] parent after join, pid={os.getpid()}")

def demo_fork():
    print(f"[fork] before fork, pid={os.getpid()}")
    pid = os.fork() # создаем дочерний процесс
    print(f"[fork] after fork, pid={os.getpid()}, returned pid={pid}")
    pid = os.fork()
    print(f"[fork] after fork, pid={os.getpid()}, returned pid={pid}")

    if pid == 0: # у дочернего процесса внутри родитьльского процесса pid == 0
        print(f"[fork] child branch, pid={os.getpid()}")
        os._exit(0)
    else:
        os.wait()
        print(f"[fork] parent branch, pid={os.getpid()}")

if __name__ == "__main__":
    method = 'fork'
    if method == 'fork':
        print("=== DEMO FORK ===")
        demo_fork()
    elif method == 'spawn':
        print("\n=== DEMO SPAWN ===")
        demo_spawn()