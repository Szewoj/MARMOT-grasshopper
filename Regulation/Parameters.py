

class PID:
    """General parameter class"""
    P = (0,0)
    I = (0,0)
    D = (0,0)
    B = (0,0)

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


class PID_PI(PID):
    """PI regulator"""
    P = (.24, .48)
    I = (.005, .01)
    B = (1.5 * I[0], 1.5 * I[1])