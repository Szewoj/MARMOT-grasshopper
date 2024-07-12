import numpy as np

class Splitter:
    """Splits pid2d outputs between 4 on-board servos"""

    def __init__(self) -> None:
        # allocate memory for faster computing:
        self._dUxy:np.ndarray = np.empty((1,2))
        self._dUsplit:np.ndarray = np.empty((1,4))
        self._splitMtx:np.ndarray = np.empty((2,4))
        self._joinMtx:np.ndarray = np.empty((4,2))
        self._om_x = 0.
        self._om_x_inv = 0.
        self._om_y = 0.
        self._om_y_inv = 0.


    def split(self, dUpid:np.ndarray, omega:tuple[float]) -> np.ndarray:
        self._om_x = omega[0]
        self._om_x_inv = omega[0] - 1
        self._om_y = omega[1]
        self._om_y_inv = omega[1] - 1

        self._splitMtx[0][0] = self._om_x
        self._splitMtx[0][1] = self._om_x_inv
        self._splitMtx[0][2] = self._om_x
        self._splitMtx[0][3] = self._om_x_inv
        self._splitMtx[1][0] = self._om_y_inv
        self._splitMtx[1][1] = self._om_y_inv
        self._splitMtx[1][2] = self._om_y
        self._splitMtx[1][3] = self._om_y

        self._dUxy[:] = dUpid
        self._dUsplit[:] = self._dUxy @ self._splitMtx
        return self._dUsplit
    

    def splitEven(self, dUpid:np.ndarray) -> np.ndarray:
        return self.split(dUpid, (.5,.5))
    

def main() -> None:
    splitter = Splitter()

    uPID = np.array([1, -1])

    print("#######################")

    print("Splitting: " + str(uPID))

    print(splitter.splitEven(uPID))
    print(splitter.split(uPID, (.4, .2)))


if __name__ == '__main__':
    main()