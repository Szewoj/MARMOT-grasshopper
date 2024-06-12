# Receive steering inputs from WiFi and set actuator outputs for:
#  - Main brushed motor
#  - Steering servo
#  - Four suspension servos

from misc.InterruptibleLoop import InterruptibleLoop
import socket, struct
import Actuator.servo as servo

HOST='0.0.0.0'
PORT=5733


def main():
    connected = False
    loop = InterruptibleLoop()

    # setup control board:
    servo.initPCA9685()

    servoLF = servo.ServoMotor(10)

    # setup radio server:
    ss:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.listen(1)
    ss.settimeout(1)

    print('Radio server started! Waiting for connection on: ' + HOST +':' + str(PORT))

    while loop.loop_again:
        # reset motors to default
        servoLF.turnOff()


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

            inputs = [int.from_bytes(data[0], signed=True),
                      int.from_bytes(data[1], signed=True),
                      int.from_bytes(data[2], signed=True),
                      int.from_bytes(data[3], signed=True),
                      int.from_bytes(data[4], signed=True),
                      int.from_bytes(data[5], signed=True)]
            print(inputs)

            # set inputs:
            servoLF.setPosition(inputs[2])
    

    # clean up after steering:
    if connected:
        s.close()
        connected = False
    ss.close()

    # reset controls
    servoLF.turnOff()

if __name__ == '__main__':
    main()