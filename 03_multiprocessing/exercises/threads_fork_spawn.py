import os
import threading
import time


# def demo_deadlock_after_fork():
#     lock = threading.Lock()

#     def holder():
#         print('inside holder thread')
#         lock.acquire()
#         print('acquired lock by first Thread')
#         time.sleep(5)
#         lock.release()

#     def forker():
#         print('inside forker thread')
#         time.sleep(1)
#         pid = os.fork()

#         if pid == 0:
#             print('child process started')
#             # print('trying to release acquired by father lock')
#             # lock.release()
#             print('trying to acquire acuqired by father lock')
#             lock.acquire()
#             print('here')
#             lock.release()
#             os._exit(0)
#         else:
#             print('hello, i am father, i am waiting for my child')
#             os.waitpid(pid, 0)
#         print('We are both here', flush=True)

#     print('STARTED MAIN')
#     t1 = threading.Thread(target=holder)
#     t2 = threading.Thread(target=forker)
#     print('threads have been initialzed')

#     t1.start()
#     t2.start()

#     t1.join()
#     t2.join()

# if __name__ == '__main__':
#     _ = demo_deadlock_after_fork()



import os
import threading
import time
import multiprocessing


def child_fork(lock):
    print('child process started', flush=True)
    # print('trying to release acquired by father lock')
    # lock.release()
    print('trying to acquire acquired-by-father lock', flush=True)
    lock.acquire()   # deadlock
    print('here', flush=True)
    lock.release()
    os._exit(0)


def child_spawn(lock):
    print('child process started', flush=True)
    print('trying to acquire passed multiprocessing lock', flush=True)
    lock.acquire()
    print('here', flush=True)
    lock.release()


def demo_fork():
    lock = threading.Lock()

    def holder():
        print('inside holder thread', flush=True)
        lock.acquire()
        print('acquired lock by first thread', flush=True)
        time.sleep(5)
        lock.release()
        print('released lock by first thread', flush=True)

    def starter():
        print('inside starter thread', flush=True)
        time.sleep(1)

        pid = os.fork()

        if pid == 0:
            child_fork(lock)
        else:
            print('hello, i am father, i am waiting for my child', flush=True)
            os.waitpid(pid, 0)

        print('we are both here', flush=True)

    print('STARTED demo_fork', flush=True)
    t1 = threading.Thread(target=holder)
    t2 = threading.Thread(target=starter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def demo_spawn():
    ctx = multiprocessing.get_context('spawn')
    lock = ctx.Lock()

    def holder():
        print('inside holder thread', flush=True)
        lock.acquire()
        print('acquired lock by first thread', flush=True)
        time.sleep(5)
        lock.release()
        print('released lock by first thread', flush=True)

    def starter():
        print('inside starter thread', flush=True)
        time.sleep(1)

        p = ctx.Process(target=child_spawn, args=(lock,))
        p.start()

        p.join()

    print('STARTED demo_spawn', flush=True)
    t1 = threading.Thread(target=holder)
    t2 = threading.Thread(target=starter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    # demo_fork()
    demo_spawn()