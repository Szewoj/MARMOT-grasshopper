

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
    """Lambda tuned pid parameters. Lambda=(.105, 0.06). Very slow."""
    P = (.0166, .0162)
    I = (0.0722, 0.1014)
    D = (0.0012, 0.00065)
    B = (0.1 * I[0], 0.1 * I[1])

    FREQ = 100  # regulation frequency
    SKIP = 2   # logger skip

class PID_LAMBDA_V2(PID):
    """Lambda tuned pid parameters. Lambda=(.105, 0.06), parameters x10. Fast, but unstable."""
    P = (.166, .162)
    I = (.722, 1.014)
    D = (.012, .0065)
    B = (0.1 * I[0], 0.1 * I[1])

    FREQ = 100  # regulation frequency
    SKIP = 2   # logger skip

class PID_X(PID):
    """Custom experimental PID parameters."""
    P = (.166, 0)
    I = (.722, 0)
    D = (.012, 0)
    B = (0.1 * I[0], 0.1 * I[1])

class PID_Y(PID):
    """Custom experimental PID parameters."""
    P = (0, .162)
    I = (0, 1.014)
    D = (0, .0065)
    B = (0.1 * I[0], 0.1 * I[1])


class PID_XY_V1(PID):
    """Custom experimental PID parameters. Faster lambda variation. Less integral.  (Version: 1)"""
    P = (.202, .194)
    I = (.361, 0.507)
    D = (.012, .0065)
    B = (0.1 * I[0], 0.1 * I[1])

    FREQ = 75  # regulation frequency
    SKIP = 1   # logger skip


class PID_XY_V2(PID):
    """Custom experimental PID parameters. Higher integral parameter.(Version: 1)"""
    P = (.195, .19)
    I = (.5415, .7605)
    D = (.0092, .0067)
    B = (0.1 * I[0], 0.1 * I[1])

    FREQ = 80  # regulation frequency
    SKIP = 3   # logger skip