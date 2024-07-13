import numpy as np


class PID2D:
    """
    2-Dimensional PID algorithm for simultaneous regulation on two channels.
    PID algorithm used is a paralel PID discretized by backward Euler method.
    """

    def __init__(self, Dt:float=1.,
                 Kp_xy:tuple[float] = (0., 0.)) -> None:
        
        # init PID parameters:
        self._Dt = Dt

        self._Kp = np.zeros((2,2))
        self._Ki = np.zeros((2,2))
        self._Td = np.zeros((2,2))

        # init calculation variables:
        self._ek = np.empty((1,2))
        self._ek_1 = np.zeros((1,2))

        self._uP = np.empty((1,2))
        self._uI = np.empty((1,2))
        self._uD = np.empty((1,2))
        self._uOut = np.empty((1,2))

        self.setKp(Kp_xy)

    
    def setDt(self, Dt:float) -> None:
        """Set calculation time interval"""
        self._Dt = Dt

    def setKp(self, Kp_xy:tuple[float]) -> None:
        """Set proportional parameter K_p for two channels."""
        if len(Kp_xy) != 2:
            print("Kp_xy parameter must be tuple with two float values!")
            return
        self._Kp[0][0] = Kp_xy[0]
        self._Kp[1][1] = Kp_xy[1]


    def update(self, e:np.ndarray) -> np.ndarray:
        if e.size != 2:
            print("Error vector must have two values!")
        self._ek[:] = e.reshape((1,2))

        self._uP[:] = self._ek @ self._uP

        self._uOut[:] = self._uP
        return self._uOut



def main() -> None:
    pid2d = PID2D()

    pid2d.setKp((.3, .5))

    print(pid2d._Kp)

if __name__ == '__main__':
    main()