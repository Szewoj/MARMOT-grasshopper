# Receive steering inputs from WiFi and set actuator outputs for:
#  - Main brushed motor
#  - Steering servo
#  - Four suspension servos

from misc.InterruptibleLoop import InterruptibleLoop
import socket, struct
import Actuator.motors as motors

HOST='0.0.0.0'
PORT=5733


def main():
    connected = False
    loop = InterruptibleLoop()

    # setup control board:
    motors.initPCA9685()

    servoLF = motors.ServoMotorInv(6, -5)
    servoRF = motors.ServoMotor(5, -15)
    servoLB = motors.ServoMotor(10)
    servoRB = motors.ServoMotorInv(11)
    servoSteering = motors.GenericMotor(7)
    brushedMotor = motors.BrushedMotor(8)

    # setup radio server:
    ss:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.listen(1)
    ss.settimeout(1)

    print('Radio server started! Waiting for connection on: ' + HOST +':' + str(PORT))

    while loop.loop_again:
        # reset motors to default
        servoLF.turnOff()
        servoRF.turnOff()
        servoLB.turnOff()
        servoRB.turnOff()
        servoSteering.turnOff()
        brushedMotor.turnOff()

        # accept client:
        try:
            s, address = ss.accept()
            connected = True
        except socket.error:
            # timeout on accept, loop again
            continue
        print("Accepted connection from " + str(address))
        print("Radio receiving...")

        s.settimeout(0.5)
        byte_data:bytes = b''
        while loop.loop_again:
            try:
                byte = s.recv(1)
            except socket.error:
                # Failed receiving data, reconnect socket
                print("Socket disconnected!")
                s.close()
                connected = False
                break

            if len(byte) == 0:
                print("Socket disconnected!")
                s.close()
                connected = False
                break

            byte_data += bytes(byte) 
            if len(byte_data) < 24:
                continue

            data = struct.unpack('!6f', byte_data)
            byte_data = b''

            inputs = [round(data[i],1) for i in range(6)]
            print(inputs)

            # set inputs:
            
            brushedMotor.setOutputAI(inputs[0])
            servoSteering.setOutputAI(inputs[1])
            servoLF.setOutputAI(inputs[2])
            servoRF.setOutputAI(inputs[3])
            servoLB.setOutputAI(inputs[4])
            servoRB.setOutputAI(inputs[5])
    

    # clean up after steering:
    if connected:
        s.close()
        connected = False
    ss.close()

    # reset controls
    servoLF.turnOff()
    servoRF.turnOff()
    servoLB.turnOff()
    servoRB.turnOff()
    servoSteering.turnOff()
    brushedMotor.turnOff()

if __name__ == '__main__':
    main()