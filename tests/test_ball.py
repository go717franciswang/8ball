import unittest
import numpy.testing as npt
import pb.ball 

class TestBall(unittest.TestCase):
    def testGetPhantomPos(self):
        # H <-- B
        ball = pb.ball.Ball(1,0,0.5)
        pos = ball.get_phantom_pos((0,0))
        npt.assert_almost_equal(pos, (2,0))

        # H
        # ^
        # |
        # B
        ball = pb.ball.Ball(0,1,0.5)
        pos = ball.get_phantom_pos((0,0))
        npt.assert_almost_equal(pos, (0,2))

        # H
        #  \
        #   B
        ball = pb.ball.Ball(1,1,0.5)
        x,y = ball.get_phantom_pos((0,0))
        npt.assert_almost_equal(x, 1.70710678)
        npt.assert_almost_equal(y, 1.70710678)
