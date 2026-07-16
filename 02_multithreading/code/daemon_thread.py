import threading, time

def worker():
    while True:
        print("working")
        time.sleep(1)

threading.Thread(target=worker, daemon=True).start()
print("main finished")
