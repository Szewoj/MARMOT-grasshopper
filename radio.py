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

    servoSteering = motors.GenericMotor(10)

    # setup radio server:
    ss:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.listen(1)
    ss.settimeout(1)

    print('Radio server started! Waiting for connection on: ' + HOST +':' + str(PORT))

    while loop.loop_again:
        # reset motors to default
        servoSteering.turnOff()


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
            if len(byte_data) < 6:
                continue

            data = struct.unpack('!6c', byte_data)
            byte_data = b''

            inputs = [int.from_bytes(data[x], byteorder='little', signed=True) for x in range(6)]
            print(inputs)

            # set inputs:
            servoSteering.setOutputAI(inputs[1])
    

    # clean up after steering:
    if connected:
        s.close()
        connected = False
    ss.close()

    # reset controls
    servoSteering.turnOff()

if __name__ == '__main__':
    main()