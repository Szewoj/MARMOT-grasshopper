import numpy as np

ZEROS = np.zeros((1,4))

class Splitter:
    """Splits pid2d outputs between 4 on-board servos"""

    def __init__(self) -> None:
        # allocate memory for faster computing:
        self._dUxy:np.ndarray = np.empty((2,1))
        self._dUsplit:np.ndarray = np.empty((4,1))
        self._splitMtx:np.ndarray = np.empty((4,2))
        self._joinMtx:np.ndarray = np.empty((2,4))
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
        self._splitMtx[0][1] = self._om_y_inv
        self._splitMtx[1][0] = self._om_x_inv
        self._splitMtx[1][1] = self._om_y_inv
        self._splitMtx[2][0] = self._om_x
        self._splitMtx[2][1] = self._om_y
        self._splitMtx[3][0] = self._om_x_inv
        self._splitMtx[3][1] = self._om_y

        self._dUxy[:] = dUpid
        self._dUsplit[:] =  self._splitMtx @ self._dUxy
        return self._dUsplit
    

    def join(self, uClamp:np.ndarray) -> np.ndarray:
        self._dUsplit[:] = uClamp.reshape((4,1))
        
        # check if uClamp has any values
        if (self._dUsplit == ZEROS).all():
            self._dUxy[:] = np.zeros((2,1))
            return self._dUxy
        
        try:
            self._joinMtx[:] = np.linalg.pinv(self._splitMtx)
            #print(self._joinMtx)
            #print(self._dUsplit)
            self._dUxy[:] = self._joinMtx @ self._dUsplit
            #print(self._dUxy)
        except np.linalg.LinAlgError as e:
            print(e)
            self._dUxy[:] = np.zeros((2,1))
        
        return self._dUxy



    def splitEven(self, dUpid:np.ndarray) -> np.ndarray:
        return self.split(dUpid, (.5,.5))
    


class Equalizer:
    """
    Class for centering mean motor output in case it drifts.
    Implemented as simple P algorithm.
    """

    CENTERPOINT = 50.0
    KP = 0.1

    def __init__(self) -> None:
        self._dU = np.empty((4,1))

    def center(self, uOut:np.ndarray) -> np.ndarray:
        self._dU[:] = np.clip(Equalizer.KP * (uOut - Equalizer.CENTERPOINT), -2, 2)
        return self._dU



def main() -> None:
    splitter = Splitter()

    uPID = np.empty((2,1))
    uPID[0] = 1
    uPID[1] = -1
    a = np.empty((4,1))

    print("#######################")

    print("Splitting: \n" + str(uPID))
    
    a[:] = splitter.splitEven(uPID)
    print("Split: \n" + str(a))
    uPID[:] = splitter.join(a)
    print("Joined: \n" + str(uPID))

    a[:] = splitter.split(uPID, (.4, .2))
    print("Split: \n" + str(a))
    uPID[:] = splitter.join(a)
    print("Joined: \n" + str(uPID))

if __name__ == '__main__':
    main()