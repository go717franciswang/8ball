class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance_btw_centers(self, ball):
        return ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5
