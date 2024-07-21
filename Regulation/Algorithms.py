import numpy as np


class PID2D:
    """
    2-Dimensional PID algorithm for simultaneous regulation on two channels.
    PID algorithm used is a paralel PID discretized by backward Euler method.
    """

    def __init__(self, Dt:float=1.,
                 Kp_xy:tuple[float, float] = (0., 0.),
                 Ki_xy:tuple[float, float] = (0., 0.),
                 Td_xy:tuple[float, float] = (0., 0.),
                 Kb_xy:tuple[float, float] = (0., 0.),
                 Kx_xy:tuple[float, float] = (0., 0.)) -> None:
        
        # init PID parameters:
        self._Dt = Dt

        self._Kp = np.zeros((2,2))  # proportional parameter P
        self._Ki = np.zeros((2,2))  # inversed integral parameter I (Ki = 1/Ti) 
                                    # - we don't use classic Ti parameter, because it complicates turning off integration
        self._Td = np.zeros((2,2))  # derivative parameter D

        self._Kb = np.zeros((2,2))  # anti-windup parameter for back-calculation algorithm

        self._Kx = np.zeros((2,2))  # crossover correction for PID output

        # init calculation variables:
        self._ek = np.empty((2,1))
        self._ek_1 = np.zeros((2,1))
        self._u_clamp = np.empty((2,1))

        self._uP = np.empty((2,1))
        self._uI = np.zeros((2,1))
        self._uD = np.empty((2,1))
        self._uOut = np.empty((2,1))

        self.setKp(Kp_xy)
        self.setKi(Ki_xy)
        self.setTd(Td_xy)
        self.setKb(Kb_xy)
        self.setKx(Kx_xy)

        self._TdBlock = True

    #---
    
    def setDt(self, Dt:float) -> None:
        """Set calculation time interval"""
        self._Dt = Dt


    def setKp(self, Kp_xy:tuple[float, float]) -> None:
        """Set proportional parameter K_p for two channels."""
        if len(Kp_xy) != 2:
            print("Kp_xy parameter must be tuple with two float values!")
            return
        self._Kp[0][0] = Kp_xy[0]
        self._Kp[1][1] = Kp_xy[1]


    def setKi(self, Ki_xy:tuple[float, float]) -> None:
        """Set integral parameter K_i (1/T_i) for two channels."""
        if len(Ki_xy) != 2:
            print("Ki_xy parameter must be tuple with two float values!")
            return
        else:
            self._Ki[0][0] = Ki_xy[0]
            self._Ki[1][1] = Ki_xy[1]


    def setTd(self, Td_xy:tuple[float, float]) -> None:
        """Set derivative parameter T_d for two channels."""
        if len(Td_xy) != 2:
            print("Td_xy parameter must be tuple with two float values!")
            return
        else:
            self._Td[0][0] = Td_xy[0]
            self._Td[1][1] = Td_xy[1]


    def setKb(self, Kb_xy:tuple[float, float]) -> None:
        """Set anti windup parameter K_b (should be ~ 1/T_i) for two channels."""
        if len(Kb_xy) != 2:
            print("Kb_xy parameter must be tuple with two float values!")
            return
        else:
            self._Kb[0][0] = Kb_xy[0]
            self._Kb[1][1] = Kb_xy[1]

    def setKx(self, Kx_xy:tuple[float, float]) -> None:
        """Set crossover correction parameter K_x for two channels."""
        if len(Kx_xy) != 2:
            print("Kx_xy parameter must be tuple with two float values!")
            return
        else:
            self._Kx[0][1] = Kx_xy[0]
            self._Kx[1][0] = Kx_xy[1]


    def update(self, e:np.ndarray) -> np.ndarray:
        if e.size != 2:
            print("Error vector e must have two values!")
        self._ek[:] = e.reshape((2,1))

        if self._TdBlock:
            self._TdBlock = False
            self._ek_1[:] = self._ek

        self._uP[:] = self._Kp @ self._ek
        self._uI[:] = self._uI + np.clip(self._Dt * (self._Ki @ self._ek), -20, 20) # clip to protect from calculation errors
        self._uD[:] = (self._Td @ (self._ek - self._ek_1)) / self._Dt

        self._ek_1[:] = self._ek

        self._uOut[:] = self._uP + self._uI + self._uD
        self._uOut[:] = np.clip(self._uOut, -50, 50) # clip output to protect from calculation errors

        # correct outputs by crossover ratio:
        self._uOut[:] = self._uOut + self._Kx @ self._uOut

        return self._uOut


    def antiWindup(self, u_clamp:np.ndarray) -> None:
        """
        Anti-windup step with back-calculation method.
        
        u_clamp should represent difference between PID output and clamped output
        """
        if u_clamp.size != 2:
            print("Error vector u_clamp must have two values!")

        self._u_clamp[:] = u_clamp.reshape((2,1))
        self._uI[:] = self._uI - np.clip(self._Kb @ self._u_clamp, -30, 30)
        


def main() -> None:
    pid2d = PID2D(Dt=0.1)

    u = np.empty((2,1))
    e = np.empty((2,1))
    e[0][0] = 1
    e[1][0] = -10

    pid2d.setKp((.3, .5))
    pid2d.setKi((.1, .1))
    pid2d.setTd((.08, .0))
    u = pid2d.update(e)

    print(pid2d._Kp)
    print(e)
    print(u)

    u = pid2d.update(e)
    print(e)
    print(u)

    u = pid2d.update(e)
    print(e)
    print(u)

    u = pid2d.update(e)
    print(e)
    print(u)

    e[0][0] = -10
    u = pid2d.update(e)
    print(e)
    print(u)

if __name__ == '__main__':
    main()