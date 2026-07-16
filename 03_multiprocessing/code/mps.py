from multiprocessing import Process
import multiprocessing
import time

def test():
    while True:
        print(multiprocessing.current_process().name)
        time.sleep(2)
        
process = Process(target=test, name='process')
process.start()
print('END')
