import socket, struct


class TCPLogger:
    HOST_ADDR = '192.168.1.48'
    HOST_PORT = 6000


    def __init__(self) -> None:
        self.s:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
    

    def connect(self) -> bool:
        self.s.connect((TCPLogger.HOST_ADDR, TCPLogger.HOST_PORT))
        self.is_connected = True
        return True


    def close(self):
        self.s.close()
        self.is_connected = False



    def isConnected(self) -> bool:
        return self.is_connected
    

    def log(self,data):
        bytes = struct.pack('!%sd' % len(data), *data)
        self.s.send(bytes)

#---

def main():
     logger = TCPLogger()
     logger.connect()
     logger.log([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
     logger.close()


#---

if __name__ == "__main__":
    main()

