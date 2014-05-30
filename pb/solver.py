class Solver:
    def __init__(self, table):
        self.table = table

    def find_optimal_cue_ball_pos(self):
        """docstring for solve"""
        pass

    def find_target_pos_and_power(self, target_ball_type):
        '''using position is probably more accurate than
           using angle since position is only subject to
           the error in position of the ball we are trying 
           to hit, while angle is also subject to error
           in position of the cue ball.
           also, it's more straightforward to compute since
           it's just the phantom ball position'''
        for hole in self.table.get_holes():
            for ball in self.table.get_target_balls(target_ball_type):
                target_pos = ball.get_phantom_pos(hole)



