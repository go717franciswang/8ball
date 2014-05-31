import numpy as np
import sys
import ball as bll

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
           it's just the phantom ball position
           power should be btw 0 and 1
           '''
        cue_ball = self.table.get_target_balls(bll.TYPE_CUE)[0]
        easiest_shot = None
        easiest_shot_difficulty = sys.float_info.max
        for hole in self.table.get_holes():
            for ball in self.table.get_target_balls(target_ball_type):
                target_pos = ball.get_phantom_pos(hole)
                if self.is_path_clear(cue_ball, target_pos) and \
                        self.is_path_clear(ball, hole):
                    difficulty = self.get_shot_difficulty(
                            ball.get_pos(), target_pos, cue_ball.get_pos())
                    if difficulty < easiest_shot_difficulty:
                        easiest_shot_difficulty = difficulty
                        easiest_shot = target_pos

        return easiest_shot, 1

    def is_path_clear(self, src_ball, dest_pos):
        src_pos = src_ball.get_pos()
        v = np.subtract(src_pos, dest_pos)
        pv = (v[1], -v[0])
        upv = pv / np.linalg.norm(pv)
        p1 = src_pos + upv*src_ball.r
        p2 = src_pos - upv*src_ball.r
        p3 = dest_pos + upv*src_ball.r
        p4 = dest_pos - upv*src_ball.r

        for ball in self.table.get_balls():
            if ball is src_ball:
                continue

            # path is clear when no intersection btw center to center
            # and edge to edge on either side
            if ball.intersect_line(p1,p3) or \
                    ball.intersect_line(p2,p4) or \
                    ball.intersect_line(src_pos, dest_pos):
                return False

        return True

    def get_shot_difficulty(self, p1, p2, p3):
        '''smaller angle usually means easier shot
           http://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
           let p1 = ball, p2 = target, p3 = cue'''
        p12 = np.linalg.norm(np.subtract(p1, p2))
        p13 = np.linalg.norm(np.subtract(p1, p3))
        p23 = np.linalg.norm(np.subtract(p2, p3))
        angle = np.arccos((p12**2 + p13**2 - p23**2) / (2*p12*p13))
        return angle

    def get_closest_open_shot(self, target_ball_type):
        closest = None
        closest_dist = float('inf')
        cue = self.table.get_target_balls(bll.TYPE_CUE)[0]
        for ball in self.table.get_target_balls(target_ball_type):
            d = cue.distance_btw_centers(ball)
            if d < closest_dist:
                closest_dist = d
                closest = ball

        return closest.get_pos(), closest_dist
