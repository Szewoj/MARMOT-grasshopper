from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time

import position



def main():
    poseOR = position.OrientationReader()
    loop = InterruptibleLoop.InterruptibleLoop()

    sync = synchronizer.Synchro(10)

    poseOR.run_async()

    sync.start()
    while loop.loop_again:
        out = poseOR.getRPY()
        print(out)

        msg = [time.time(), out[2], out[1], 0., 0., 0., 50., 50., 50., 50.]

        sync.waitNext()

    poseOR.close()



if __name__ == "__main__":
    main()