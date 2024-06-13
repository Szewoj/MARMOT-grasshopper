import time
import random
import InterruptibleLoop

class Synchro:

    def __init__(self, freq:float) -> None:
        self.INTERVAL = 1./freq
        self.then = time.perf_counter()
        self.timeCounter = 0

    def start(self, timestamp:float=0) -> None:
        if timestamp == 0:
            timestamp = time.perf_counter()
        self.then = timestamp

    def waitNext(self) -> None:
        now = time.perf_counter()
        t_elapsed = now - self.then
        t_target = self.timeCounter + self.INTERVAL
        if t_elapsed < t_target:
            self.waitTime = t_target - t_elapsed
        else:
            self.waitTime = 0
        self.timeCounter += self.INTERVAL
        time.sleep(self.waitTime)


    def getwaitTime(self) -> float:
        return self.waitTime
    


if __name__ == '__main__':

    print("Synchro test: ")
    time.sleep(2)
    FREQ = 208
    sync = Synchro(FREQ)

    loop = InterruptibleLoop.InterruptibleLoop()

    then = time.perf_counter()
    sync.start()
    while loop.loop_again:
        calcTime = 0.003 * random.random()
        time.sleep(calcTime)

        sync.waitNext()

        now = time.perf_counter()
        print(now - then)
        then = now

