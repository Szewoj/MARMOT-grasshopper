from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time

import position



def main():
    poseOR = position.OrientationReader()
    loop = InterruptibleLoop.InterruptibleLoop()
    logger = Logger.TCPLogger(skip=2)

    sync = synchronizer.Synchro(10)

    poseOR.run_async()
    logger.run_async()

    sync.start()
    while loop.loop_again:
        out = poseOR.getRPY()
        z = poseOR.getAccZ()
        print(z)

        msg = [time.time(), out[0], out[1], z, 0., 0., 50., 50., 50., 50.]
        logger.log(msg)

        sync.waitNext()

    poseOR.close()



if __name__ == "__main__":
    main()