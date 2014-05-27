from matplotlib import pyplot as plt

class Table:
    def __init__(self, w, h):
        self._ball_in_hand = False
        self._hand_pos = None
        self._w = w
        self._h = h
        self.balls = []

    def set_ball_in_hand(self, ball_in_hand):
        self._ball_in_hand = ball_in_hand

    def set_hand(self, hand_pos):
        self._hand_pos = hand_pos

    def get_hand(self):
        return self._hand_pos

    def is_ball_in_hand(self):
        return self._ball_in_hand

    def get_balls(self):
        return self.balls

    def add_ball(self, ball):
        self.balls.append(ball)

    def does_collide(self, ball):
        # bruteforce since so few balls, perhaps use 2d binary tree for optimization if needed
        for existing in self.balls:
            if existing.distance_btw_centers(ball) < existing.r + ball.r:
                return True
        return False

