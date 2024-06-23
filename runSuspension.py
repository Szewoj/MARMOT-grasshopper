from misc import Logger, InterruptibleLoop, synchronizer

import position



def main():
    poseOR = position.OrientationReader()
    loop = InterruptibleLoop.InterruptibleLoop()

    sync = synchronizer.Synchro(5)

    poseOR.run_async()

    sync.start()
    while loop.loop_again:
        out = poseOR.getRPY()
        print(out)
        sync.waitNext()

    poseOR.close()



if __name__ == "__main__":
    main()