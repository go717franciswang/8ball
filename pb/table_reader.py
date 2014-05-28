import cv2
import numpy as np
from table import Table
from matplotlib import pyplot as plt
from game_reader import GameReader, ItemNotFound
from ball import Ball, TYPE_PHANTOM

BALL_RADIUS = 8

class TableReader:
    def __init__(self, img, debug=False):
        self.original = img.copy()
        self.debug = debug
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._dominant_color_range = None

    def get_dominant_color_range(self):
        if self._dominant_color_range is None:
            bounds = [[], []]
            for i in xrange(3):
                hist, bins = np.histogram(self.hsv[:,:,i], 100)
                samples = float(np.sum(hist))
                maxarg = np.argmax(hist)
                min_bound = maxarg
                max_bound = maxarg

                while min_bound > 0:
                    min_bound -= 1
                    if hist[min_bound] / samples < 0.005:
                        min_bound += 1
                        break

                while max_bound < 99:
                    if hist[max_bound] / samples < 0.005:
                        max_bound -= 1
                        break
                    max_bound += 1

                bounds[0].append(np.int(bins[min_bound]))
                bounds[1].append(np.int(bins[max_bound+1]))
            self._dominant_color_range = map(tuple, bounds)
        return self._dominant_color_range

    def get_masked_background(self):
        l,u = self.get_dominant_color_range()
        masked = cv2.inRange(self.hsv, l, u)
        # plt.imshow(masked)
        # plt.show()
        return masked

    def get_masked_black(self):
        masked = cv2.inRange(self.hsv, (0,0,50), (360,360,100))
        # plt.imshow(masked)
        # plt.show()
        return masked

    def get_masked(self):
        masked = cv2.bitwise_or(self.get_masked_background(), self.get_masked_black())
        # plt.imshow(masked)
        # plt.show()
        return masked

    def get_circles(self):
        masked = self.get_masked_black()
        # masked = cv2.medianBlur(masked,3)
        # masked = cv2.blur(masked,(3,3))
        masked_inv = cv2.bitwise_not(masked)

        img2 = cv2.bitwise_not(self.gray, mask=masked_inv)
        # plt.imshow(img2)
        # plt.show()
        return self._get_circles_from_img(img2)

    def _get_circles_from_img(self, img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.blur(img, (4,4))
        # img = cv2.medianBlur(img,3)
        circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,5, 
                param1=100,param2=10,minRadius=6,maxRadius=10)
        # print circles

        circles = np.uint16(np.around(circles))
        return circles

    def _is_ball_in_hand(self):
        try:
            self._hand_pos = GameReader()._get_location_from_img(
                    self.gray, 'ball in hand', threshold=0.9)
            return True
        except ItemNotFound:
            return False

    def _update_ball_detail(self, ball, table):
        x0 = max(ball.x-BALL_RADIUS,0)
        x1 = min(ball.x+BALL_RADIUS,table.h-1)
        y0 = max(ball.y-BALL_RADIUS,0)
        y1 = min(ball.y+BALL_RADIUS,table.w-1)
        ball_area = self.hsv[y0:y1, x0:x1]
        if self._is_phantom(ball_area):
            ball.type = TYPE_PHANTOM
            return

    def _is_phantom(self, ball_area):
        l,u = self.get_dominant_color_range()
        masked = cv2.inRange(ball_area, l, u)
        return np.count_nonzero(masked) / float(masked.size) > 0.35

    def get_table(self):
        size = self.original.shape
        table = Table(size[0], size[1])
        if self._is_ball_in_hand():
            table.set_ball_in_hand(True)
            table.set_hand(self._hand_pos)

        circles = self.get_circles()
        for c in circles[0,:]:
            ball = Ball(
                    x=int(np.round(c[0])), 
                    y=int(np.round(c[1])), 
                    r=BALL_RADIUS)
            if table.does_collide(ball):
                continue

            self._update_ball_detail(ball, table)
            if ball.type == TYPE_PHANTOM:
                continue

            table.add_ball(ball)

        if self.debug:
            for b in table.get_balls():
                cv2.circle(self.original,(b.x, b.y), b.r,(0,255,0),2)
                cv2.circle(self.original,(b.x, b.y),2,(0,0,255),3)

            self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
            plt.imshow(self.original)
            plt.show()

        return table

if __name__ == '__main__':
    for i in xrange(1,5):
        img = cv2.imread('resources/table%d.jpg' % (i,))
        table = TableReader(img)
        table.get_gray_img_no_background()

