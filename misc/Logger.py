import socket, struct
import queue, threading

from misc.InterruptibleLoop import InterruptibleLoop


class TCPLogger:

    def __init__(self, host='0.0.0.0', port=6000) -> None:
        self.host = host
        self.port = port

        self.s:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._connection_lock:threading.Lock = threading.Lock()
        self.is_connected = False
        self.conn:socket.socket = None

        self._th:threading.Thread = None

        self._queue:queue.Queue = None

        self._thread_loop:bool = None


    def run(self) -> None:
        self.s.bind((self.host, self.port))
        self.s.listen(1)
        self.s.settimeout(5)

        print("Logger thread started!")

        self._thread_loop = True
        while self._thread_loop:

            # accept client:
            try:
                self.conn, address = self.s.accept()
            except socket.error as e:
                # timeout on accept, loop again
                continue
            print("Accepted connection from " + str(address))
            print("Logger ready!")

            self._queue = queue.Queue(5)
            self._setConnection()
            self.conn.settimeout(1)

            while self._thread_loop:

                try:
                    data = self._queue.get(timeout=1)
                except queue.Empty as e:
                    # queue is empty, check signals:
                    continue

                # send data from queue through socket
                byte_data = struct.pack('!%sd' % len(data), *data)
                try:
                    self.conn.send(byte_data)
                except socket.error as e:
                    # Failed sending data, reconnect socket
                    print("Socket disconnected!")
                    self._clearConnection()
                    self.conn.close()
                    break
        
        # cleanup after interrupt
        if self.isConnected():
            print("Socket disconnected!")
            self._clearConnection()
            self.conn.close()
        
        self.s.close()
        print("Logger thread closed")


    def run_async(self) -> None:
        self._th = threading.Thread(target=self.run)
        self._th.start()

    def close(self):
        self._thread_loop = False
        

    def _setConnection(self) -> None:
        self._connection_lock.acquire()
        self.is_connected = True
        self._connection_lock.release()

    def _clearConnection(self) -> None:
        self._connection_lock.acquire()
        self.is_connected = False
        self._connection_lock.release()

    def isConnected(self) -> bool:
        self._connection_lock.acquire()
        retval = self.is_connected
        self._connection_lock.release()
        return retval
    

    def log(self,data):
        if self.isConnected():
            try:
                self._queue.put_nowait(data)
            except queue.Full as e:
                return


