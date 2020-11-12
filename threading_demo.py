import threading
threads = []

for i in range(0,10):
    threads.append( threading.Thread(target=nguyento) )
    # dinh nghia action cua thread
for thread in threads:
    thread.start()

threads[0].join()
