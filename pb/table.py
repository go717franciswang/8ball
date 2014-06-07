from matplotlib import pyplot as plt
import ball as bll

MAX_BALL_COUNT_BY_TYPE = {
        bll.TYPE_CUE: 1,
        bll.TYPE_BLACK: 1,
        bll.TYPE_STRIPE: 14, # using twice the correct number for now
        bll.TYPE_SOLID: 14,
        bll.TYPE_PHANTOM: 1,
        }

class Table:
    def __init__(self, w, h):
        self._ball_in_hand = False
        self._hand_pos = None
        self.w = w
        self.h = h
        self.balls = []
        self.type_balls = {}

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
        max_ball_count = MAX_BALL_COUNT_BY_TYPE.get(ball.type)
        if max_ball_count is None:
            raise Exception('Unknown ball type: %s' % (ball.type,))

        if not self.type_balls.has_key(ball.type):
            self.type_balls[ball.type] = []

        if len(self.type_balls[ball.type]) < max_ball_count:
            self.type_balls[ball.type].append(ball)
        else:
            raise Exception('Already got %d balls of type: %s' % \
                    (max_ball_count, ball.get_ball_type_str()))

        self.balls.append(ball)

    def does_collide(self, ball):
        # bruteforce since so few balls, perhaps use 2d binary tree for optimization if needed
        for existing in self.balls:
            if existing.distance_btw_centers(ball) < existing.r + ball.r - 4:
                return True
        return False

    def get_holes(self):
        '''the 2 middle holes should be placed somewhere 
           outside of the table, so that balls close the 
           rail cannot score in them'''
        return ((0, 0),
                (self.w, 0),
                (0, self.h),
                (self.w, self.h),
                (self.w/2, -self.h*0.05),
                (self.w/2, self.h*1.05))

    def get_target_balls(self, ball_type):
        if not self.type_balls.has_key(ball_type):
            raise Exception("ball type: %d cannot be found on the table" % (ball_type,))

        return self.type_balls[ball_type]

