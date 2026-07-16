import multiprocessing
from multiprocessing import Process, Queue
import os
import time
import pickle

def producer(q):
    print(f"[producer pid={os.getpid()}] put data")
    print(q, '--- queue in producer')
    q.put({"value": 42})
    print(f"[producer pid={os.getpid()}] done")

def consumer(q):
    print(f"[consumer pid={os.getpid()}] waiting...")
    print(q, '--- queue in consumer')
    data = q.get()
    print(f"[consumer pid={os.getpid()}] got:", data)

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    q = Queue()
    #d = pickle.dumps(q)
    #print(d, '--- pickle dump')

    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    p2.start()
    time.sleep(1)
    p1.start()

    p1.join()
    p2.join()
