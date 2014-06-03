import unittest
import numpy.testing as npt
import pb.solver
import pb.table
import pb.ball
import pb.table_viewer

class TestSolver(unittest.TestCase):
    def setUp(self):
        self.tv = pb.table_viewer.TableViewer()

    def testStraightShot(self):
        table = pb.table.Table(100,100)
        black = pb.ball.Ball(50,20,5,pb.ball.TYPE_BLACK) # in the middle
        table.add_ball(black)

        cue = pb.ball.Ball(50,50,5,pb.ball.TYPE_CUE)
        table.add_ball(cue)

        solver = pb.solver.Solver(table)
        target, power = solver.find_target_pos_and_power(pb.ball.TYPE_BLACK)
        npt.assert_almost_equal(target, (50,30))
        
        table.add_ball(pb.ball.Ball(target[0], target[1], 5, pb.ball.TYPE_PHANTOM))
        self.tv.display(table, block=True)

    def testShotBlocked(self):
        # A and B blocks each other from scoring in the middle
        table = pb.table.Table(100,100)
        A = pb.ball.Ball(51,20,5,pb.ball.TYPE_SOLID)
        table.add_ball(A)
        B = pb.ball.Ball(50,40,5,pb.ball.TYPE_SOLID)
        table.add_ball(B) 

        cue = pb.ball.Ball(50,60,5,pb.ball.TYPE_CUE)
        table.add_ball(cue)

        solver = pb.solver.Solver(table)
        target, power = solver.find_target_pos_and_power(pb.ball.TYPE_SOLID)
        npt.assert_almost_equal(target, (57.8086881, 46.2469505))

        table.add_ball(pb.ball.Ball(target[0], target[1], 5, pb.ball.TYPE_PHANTOM))
        self.tv.display(table, block=True)
