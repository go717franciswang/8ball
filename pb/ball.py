import numpy as np

TYPE_CUE = 0
TYPE_PHANTOM = 1
TYPE_BLACK = 2
TYPE_SOLID = 3
TYPE_STRIPE = 4

class Ball:
    def __init__(self, x, y, r, t=None):
        self.x = x
        self.y = y
        self.r = r
        self.type = t

    def distance_btw_centers(self, ball):
        return ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5

    def get_phantom_pos(self, hole_pos):
        xh,yh = hole_pos
        v = (self.x - xh, self.y - yh)
        uv = v / np.linalg.norm(v)
        return (self.x, self.y) + 2*uv*self.r

    def get_ball_type_str(self):
        if self.type == 0:
            return 'CUE'
        elif self.type == 1:
            return 'PHANTOM'
        elif self.type == 2:
            return 'BLACK'
        elif self.type == 3:
            return 'SOLID'
        elif self.type == 4:
            return 'STRIPE'
        else:
            raise Exception('Unknow ball_type_id: %s' % (self.type))

    def get_pos(self):
        return (self.x, self.y)

    def intersect_line(self, e, l):
        '''http://stackoverflow.com/questions/1073336/circle-line-collision-detection'''
        d = np.subtract(l, e)
        f = np.subtract(e, self.get_pos())

        a = np.inner(d, d)
        b = 2*np.inner(f, d)
        c = np.inner(f, f) - self.r**2
        discriminant = b*b-4*a*c

        if discriminant < 0:
            return False

        discriminant = discriminant**0.5
        t1 = (-b - discriminant)/(2*a)
        t2 = (-b + discriminant)/(2*a)

        return (0<=t1<=1) or (0<=t2<=1)

