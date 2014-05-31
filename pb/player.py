from pymouse import PyMouse
import position
import numpy as np

class Player:
    def __init__(self):
        self.mouse = PyMouse()

    def click(self, pos):
        self.mouse.click(*pos)

    def shoot(self, target, power, table_offset, cue_ball):
        adj_target = np.add(target, table_offset)
        self.mouse.press(*adj_target)

        adj_cue = np.add(cue_ball.get_pos(), table_offset)
        self.mouse.drag(*adj_cue)
        self.mouse.release(*adj_cue)

