from multiprocessing import Process, Pipe

def worker(conn):
    # conn — конец pipe в дочернем процессе
    data = conn.recv()          # ждём данные
    conn.send(data * 2)         # отвечаем
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    # parent_conn, chinld_conn - концы pipe'а, внутри хранят fd 
    print(child_conn)
    
    p = Process(target=worker, args=(child_conn,))
    p.start()

    parent_conn.send(10)        # отправка
    print(parent_conn.recv())  # получение

    p.join()
    print('here')
