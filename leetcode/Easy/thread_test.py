#!/usr/bin/python

import threading
import time

class THREAD():
    def one(self):
        for i in range(5):
            print("one thread:%d" %i)
            time.sleep(1)

t = threading.Thread(target = THREAD().one)
t.start()

for i in range(3):
    print("Main thread:%d" %i)
    time.sleep(1)

t.join()

print("Done.")
