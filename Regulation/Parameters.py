

class PID:
    """General parameter class"""
    P = (0,0)
    I = (0,0)
    D = (0,0)
    B = (0,0)
    X = (-0.0588, -0.0132)  # calculated optimal crossover ratio

    FREQ = 25  # regulation frequency
    SKIP = 0   # logger skip

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

class PID_LAMBDA_V1(PID):
    """Lambda tuned pid parameters. Lambda=(.105, 0.06) """
    P = (.0166, .0162)
    I = (4.3478, 6.25)
    D = (0.07, 0.04)
    B = (0.1 * I[0], 0.1 * I[1])

    FREQ = 100  # regulation frequency
    SKIP = 4   # logger skip

class PID_X(PID):
    """Custom experimental PID parameters."""
    P = (.42, 0)
    I = (.06, 0)
    D = (0.03, 0)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_Y(PID):
    """Custom experimental PID parameters."""
    P = (0, .435)
    I = (0, .064)
    D = (0, 0.035)
    B = (1.5 * I[0], 1.5 * I[1])


class PID_XY_V1(PID):
    """Custom experimental PID parameters. Mostly P regulation. (Version: 1)"""
    P = (.53, .57)
    I = (.08, .085)
    D = (0.008, 0.0085)
    B = (0.1 * I[0], 0.1 * I[1])


class PID_XY_V2(PID):
    """Custom experimental PID parameters. High integral parameter. (Version: 2)"""
    P = (.33, .48)
    I = (0.4, .36)
    D = (0.01, 0.012)
    B = (0.1 * I[0], 0.1 * I[1])


class PID_XY(PID):
    """Custom experimental PID parameters. Suspension frequency = 50Hz. (Version: 3)"""
    P = (.165, .24)
    I = (0.2, .18)
    D = (0.01, 0.012)
    B = (0.1 * I[0], 0.1 * I[1])

    F = 50
    S = 1