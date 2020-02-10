import sys
import multiprocessing
import threading
import hashlib
# create set of start/end numbers
# in thread function pop from set after blocking
# use sha

start = 0
end = 100
sequence = 10
pairs = []
stop = False #flag to stop the threads
hashCryptoInt = sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize

class WorkerThread(threading.Thread):
    def __init__(self,*args):
        super(WorkerThread,self).__init__()

    def run(self):
        global stop
        global hashCryptoInt
        global pairs
        while True:
            try :
                rangePair = pairs.pop()
                for x in range(rangePair[0], rangePair[1]):
                    if stop:
                        return
                    hashHex = hashlib.sha256(str(x).encode('utf-8')).hexdigest()
                    hashInt = int(hashHex,base=16)
                    #print("hashHex: " + str(hashHex) + ", hashInt: " + str(hashInt))
                    if hashInt < hashCryptoInt:
                        print("Found input: " + str(x))
                        stop = True
                        return  
            except IndexError:
                print("Index Out of Range")
                return

if __name__ == "__main__": 
    previous = start
    for x in range(start, end, sequence):
        pairs.append([previous, x])
        previous = x + 1
    threads = []
    for _ in range(3): # each Process creates a number of new Threads
        thread = WorkerThread() 
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
