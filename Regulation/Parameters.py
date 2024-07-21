

class PID:
    """General parameter class"""
    P = (0,0)
    I = (0,0)
    D = (0,0)
    B = (0,0)
    X = (-0.0588, -0.0132)  # calculated optimal crossover ratio

class PID_P(PID):
    """P regulator"""
    P = (.6, .65)

class PID_I_TEST(PID):
    """I testing parameters"""
    I = (.005, .005)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_D_TEST(PID):
    """D testing parameters"""
    D = (0.5, 0.5)


class PID_ZN(PID):
    """Ziegler-Nichols parameters of an open-loop system"""
    P = (2.7143, 3.6031)
    I = (2.302, 1.7346)
    D = (0.1086, 0.1441)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_ZN_PI(PID):
    """PI regulator"""
    P = (2.0357, 2.7023)
    I = (1.8607, 1.4017)
    B = (1.5 * I[0], 1.5 * I[1])


class PID_ZN_HALVED(PID):
    """Ziegler-Nichols parameters halved to compensate for 2d PID application"""
    P = (2.7143/2, 3.6031/2)
    I = (2.302/2, 1.7346/2)
    D = (0.1086/2, 0.1441/2)
    B = (1.5 * I[0], 1.5 * I[1])


class PID_X(PID):
    """Custom experimental PID parameters"""
    P = (.42, 0)
    I = (.06, 0)
    D = (0.03, 0)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_Y(PID):
    """Custom experimental PID parameters"""
    P = (0, .435)
    I = (0, .064)
    D = (0, 0.035)
    B = (1.5 * I[0], 1.5 * I[1])


class PID_XY_V1(PID):
    """Custom experimental PID parameters. (Version: 1)"""
    P = (.53, .57)
    I = (.08, .085)
    D = (0.008, 0.0085)
    B = (1.5 * I[0], 1.5 * I[1])


class PID_XY(PID):
    """Custom experimental PID parameters. (Version: 2)"""
    P = (.33, .48)
    I = (0.4, .36)
    D = (0.01, 0.012)
    B = (0.1 * I[0], 0.1 * I[1])