import signal

class InterruptibleLoop:
  loop_again = True
  def __init__(self):
    signal.signal(signal.SIGINT, self.break_loop_sig)
    signal.signal(signal.SIGTERM, self.break_loop_sig)

  def break_loop_sig(self, signum, frame):
    self.loop_again = False
    print("Interrupt signal received! Exiting...")

  def breakLoop(self) -> None:
    self.loop_again = False