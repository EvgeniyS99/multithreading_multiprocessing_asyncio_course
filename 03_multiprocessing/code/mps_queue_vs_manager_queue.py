import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def run(q):
    print('get queue')

def main():
    q = mp.Queue(maxsize=2)
    with ProcessPoolExecutor(max_workers=2) as ex:
        future = ex.submit(run, q)
        result = future.result()
    print(result)

if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    main()