import cv2
from matplotlib import pyplot as plt
import numpy as np
import ball as bll

class TableViewer:
    def display(self, table, block=False):
        img = np.zeros(shape=(table.w, table.h, 3), dtype='uint8')
        img[:,:,1] = np.ones(shape=(table.w, table.h), dtype='uint8') * 255

        for ball in table.get_balls():
            pos = tuple(map(np.int, np.round(ball.get_pos())))
            r = ball.r
            if ball.type == bll.TYPE_CUE:
                cv2.circle(img, pos, r, (255,255,255), lineType=cv2.CV_AA)
            elif ball.type == bll.TYPE_BLACK:
                cv2.circle(img, pos, r, (0,0,0), lineType=cv2.CV_AA)
            elif ball.type == bll.TYPE_STRIPE:
                cv2.circle(img, pos, r, (255,0,0), lineType=cv2.CV_AA)
            elif ball.type == bll.TYPE_SOLID:
                cv2.circle(img, pos, r, (0,0,255), lineType=cv2.CV_AA)
            elif ball.type == bll.TYPE_PHANTOM:
                cv2.circle(img, pos, r, (128,128,128), lineType=cv2.CV_AA)

        plt.imshow(img)
        plt.draw()
        plt.show(block=block)

if __name__ == '__main__':
    import table
    t = table.Table(200, 300)
    t.add_ball(bll.Ball(150,100,9,bll.TYPE_CUE))
    t.add_ball(bll.Ball(250,100,9,bll.TYPE_BLACK))
    t.add_ball(bll.Ball(250,50,9,bll.TYPE_STRIPE))
    t.add_ball(bll.Ball(250,150,9,bll.TYPE_SOLID))
    t.add_ball(bll.Ball(232,100,9,bll.TYPE_PHANTOM))
    table_viewer = TableViewer()
    table_viewer.display(t, True)

