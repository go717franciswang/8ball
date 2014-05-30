import numpy as np

TYPE_CUE = 0
TYPE_PHANTOM = 1
TYPE_BLACK = 2
TYPE_SOLID = 3
TYPE_STRIPE = 4

class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.type = None

    def distance_btw_centers(self, ball):
        return ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5

    def get_phantom_pos(self, hole_pos):
        xh,yh = hole_pos
        v = (self.x - xh, self.y - yh)
        uv = v / np.linalg.norm(v)
        return (self.x, self.y) + 2*uv*self.r
