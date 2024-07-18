

class PID:
    """General parameter class"""
    P = (0,0)
    I = (0,0)
    D = (0,0)
    B = (0,0)

class PID_P(PID):
    """P regulator"""
    P = (2.4, 4.8)

class PID_I_TEST(PID):
    """I testing parameters"""
    I = (.2, .2)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_D_TEST(PID):
    """D testing parameters"""
    D = (0.1, 0.1)

