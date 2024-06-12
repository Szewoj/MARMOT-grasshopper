import signal

class InterruptibleLoop:
  loop_again = True
  def __init__(self):
    signal.signal(signal.SIGINT, self.break_loop)
    signal.signal(signal.SIGTERM, self.break_loop)

  def break_loop(self, signum, frame):
    self.loop_again = False
    print("Interrupt signal received! Exiting...")