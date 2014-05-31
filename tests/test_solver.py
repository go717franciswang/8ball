import unittest
import numpy.testing as npt
import pb.solver
import pb.table
import pb.ball

class TestSolver(unittest.TestCase):
    def testStraightShot(self):
        table = pb.table.Table(10,10)
        black = pb.ball.Ball(5,2,0.5,pb.ball.TYPE_BLACK) # in the middle
        table.add_ball(black)

        cue = pb.ball.Ball(5,5,0.5,pb.ball.TYPE_CUE)
        table.add_ball(cue)

        solver = pb.solver.Solver(table)
        target, power = solver.find_target_pos_and_power(pb.ball.TYPE_BLACK)
        npt.assert_almost_equal(target, (5,3))

    def testShotBlocked(self):
        # A and B blocks each other from scoring in the middle
        table = pb.table.Table(10,10)
        A = pb.ball.Ball(5.1,2,0.5,pb.ball.TYPE_SOLID)
        table.add_ball(A)
        B = pb.ball.Ball(5,4,0.5,pb.ball.TYPE_SOLID)
        table.add_ball(B) 

        cue = pb.ball.Ball(5,6,0.5,pb.ball.TYPE_CUE)
        table.add_ball(cue)

        solver = pb.solver.Solver(table)
        target, power = solver.find_target_pos_and_power(pb.ball.TYPE_SOLID)
        npt.assert_almost_equal(target, (5.78086881, 4.62469505))

