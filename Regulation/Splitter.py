import numpy as np

# split constants:
ZEROS = np.zeros((1,4))

# centering constants:
P_LIMIT = np.matrix([[0.],[100.]])
N_LIMIT = np.matrix([[100.],[0.]])

# Z axis split constants:
Z_P = np.matrix('5., .0; .0, 6.')
Z_D0 = np.matrix('1., .0; .0, -1.')
Z_M = np.empty((2,2))
Z_M[:] = Z_P @ Z_D0

class Splitter:
    """Splits pid2d outputs between 4 on-board servos"""

    def __init__(self) -> None:
        # allocate memory for faster computing:
        self._dUxy:np.ndarray = np.empty((2,1))
        self._dUsplit:np.ndarray = np.empty((4,1))
        self._u:np.ndarray = np.empty((4,1))
        """Output values [uFL, uFR, uBL, uBR]"""
        self._p:np.ndarray = np.empty((2,1))
        self._mx:np.ndarray = np.empty((2,1))
        """mean vector of x axis outputs [Right, Left]"""
        self._my:np.ndarray = np.empty((2,1))
        """mean vector of x axis outputs [Front, Back]"""
        self._zSplit:np.ndarray = np.empty((2,1))
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
    

    def centeringOmega(self, dUpid:np.ndarray, u:np.ndarray) -> tuple[float, float]:
        self._u[:] = u
        self._p[:] = dUpid

        self._mx[0][0] = np.mean(self._u[[1,3]])
        self._mx[1][0] = np.mean(self._u[[0,2]])
        self._my[0][0] = np.mean(self._u[[0,1]])
        self._my[1][0] = np.mean(self._u[[2,3]])

        if np.signbit(self._p[0][0]):
            # negative dUx
            self._mx[:] = np.clip(np.abs(N_LIMIT - self._mx), .1, None)
        else:
            # positive dUx
            self._mx[:] = np.clip(np.abs(P_LIMIT - self._mx), .1, None)

        if np.signbit(self._p[1][0]):
            # negative dUy
            self._my[:] = np.clip(np.abs(N_LIMIT - self._my), .1, None)
        else:
            # positive dUy
            self._my[:] = np.clip(np.abs(P_LIMIT - self._my), .1, None)
        
        om_x = round(self._mx.tolist()[1][0] / self._mx.sum(), 2)
        om_y = round(self._my.tolist()[1][0] / self._my.sum(), 2)

        return (om_x, om_y)


    def splitCentering(self, dUpid:np.ndarray, u:np.ndarray) -> np.ndarray:
        spl = self.centeringOmega(dUpid, u)
        spl_centered = (0.1 + 0.8 * spl[0], 0.1 + 0.8 * spl[1])
        return self.split(dUpid, spl_centered)
    

    def splitByZ(self, dUpid:np.ndarray, u:np.ndarray, vZ:float) -> np.ndarray:
        baseSplit = self.centeringOmega(dUpid, u) # base split for keeping output away from limits

        # calculate split based on z axis velocity:
        self._dUxy[:] = np.round(dUpid,1)

        self._zSplit[:] = np.clip(Z_M @ np.sign(self._dUxy) * vZ + .5, 0.05, 0.95)

        print(self._zSplit)
        
        om_x = round(.5 * baseSplit[0] + .5 * self._zSplit.tolist()[0][0] , 2)
        om_y = round(.5 * baseSplit[1] + .5 * self._zSplit.tolist()[1][0] , 2)

        return self.split(dUpid, (om_x, om_y))

class Equalizer:
    """
    Class for centering mean motor output in case it drifts.
    Implemented as simple P algorithm.
    """

    CENTERPOINT = 50.0
    KP = 0.05

    def __init__(self) -> None:
        self._dU = np.empty((4,1))
        self._e = .0

    def center(self, uOut:np.ndarray) -> np.ndarray:
        self._e = Equalizer.CENTERPOINT - np.mean(uOut)
        self._dU.fill(np.clip(Equalizer.KP * self._e, -2, 2))
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

    print("#######################")

    print("Generate split data for:")
    uPID[0] = 1
    uPID[1] = -1
    print(uPID)
    a = np.matrix('80.; 40.; 80.; 40.')
    print('')

    print(splitter.centeringOmega(uPID, a))

    print("#######################")
    print("Split by Z=2:")
    uPID[0] = 0
    uPID[1] = 10
    print(uPID)
    a = np.matrix('0.; 0.; 50.; 50.')
    print('')

    print(splitter.splitByZ(uPID, a, 2.))

if __name__ == '__main__':
    main()