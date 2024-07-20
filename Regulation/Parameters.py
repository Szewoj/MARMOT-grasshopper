

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


class PID_ZN(PID):
    """Ziegler-Nichols parameters of an open-loop system"""
    P = (2.7143, 3.6031)
    I = (2.3026, 1.7346)
    D = (0.1086, 0.1441)
    B = (1.5 * I[0], 1.5 * I[1])

class PID_ZN_PI(PID):
    """PI regulator"""
    P = (2.0357, 2.7023)
    I = (1.8607, 1.4017)
    B = (1.5 * I[0], 1.5 * I[1])