import struct
from inputs import get_gamepad
import math, socket, threading
from time import sleep
from misc.InterruptibleLoop import InterruptibleLoop

MARMOT_IP = '192.168.1.101'
MARMOT_C_PORT = 5733


def deadzone(input:float, deadzone):
    if input > 0:
        return max(0, (input - deadzone) / (1. - deadzone))
    else:
        return min(0, (input + deadzone) / (1. - deadzone))



class XboxController:
    # XboxController class by Brian Zier and Kevin Hughes. (2017 MIT-license)
    # https://github.com/bzier/TensorKart/blob/master/utils.py
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self):
        xL = deadzone(self.LeftJoystickX, 0.2)
        yL = deadzone(self.LeftJoystickY, 0.2)
        xR = deadzone(self.RightJoystickX, 0.2)
        yR = deadzone(self.RightJoystickY, 0.2)
        trig = deadzone(self.RightTrigger, 0.07) - deadzone(self.LeftTrigger, 0.07)

        # translate to mobile base control signals:
        throttle = round(trig*100)
        steering = round(xL*100)

        updown = round(yL * 100 / 2)
        xAxis = round(xR * 100 / 2)
        yAxis = round(yR * 100 / 2)

        uFL = min(100, max(0, 50 + updown + xAxis - yAxis))
        uFR = min(100, max(0, 50 + updown - xAxis - yAxis))
        uBL = min(100, max(0, 50 + updown + xAxis + yAxis))
        uBR = min(100, max(0, 50 + updown - xAxis + yAxis))

        return [throttle, steering, uFL, uFR, uBL, uBR]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state



def main():
    joy = XboxController()
    loop = InterruptibleLoop()

    try:
        s:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((MARMOT_IP, MARMOT_C_PORT))
        
        while loop.loop_again:
            sleep(0.1)
            data = joy.read()
            byte_data = struct.pack('!%sb' % len(data), *data)
            s.send(byte_data)

    except socket.error:
        print('Lost connection, exiting...')
    finally:
        s.close()


if __name__ == '__main__':
    main()
    