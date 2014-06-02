import cv2
import numpy as np
from table import Table
from matplotlib import pyplot as plt
import game_reader
import ball as ball_mod

BALL_RADIUS = 8
BALL_ROI = np.zeros((BALL_RADIUS*2+1, BALL_RADIUS*2+1), dtype='uint8')
for i in range(BALL_RADIUS*2+1):
    for j in range(BALL_RADIUS*2+1):
        if ((i-BALL_RADIUS)**2 + (j-BALL_RADIUS)**2)**0.5 <= BALL_RADIUS:
            BALL_ROI[i,j] = 255

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
        masked = cv2.inRange(self.hsv, (0,0,50), (180,256,100))
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
            self._hand_pos = game_reader.GameReader()._get_location_from_img(
                    self.gray, 'ball in hand', threshold=0.9)
            return True
        except game_reader.ItemNotFound:
            return False

    def _update_ball_detail(self, ball, table):
        x0 = max(ball.x-BALL_RADIUS,0)
        x1 = min(ball.x+BALL_RADIUS+1,table.h)
        y0 = max(ball.y-BALL_RADIUS,0)
        y1 = min(ball.y+BALL_RADIUS+1,table.w)
        ball_area = self.hsv[y0:y1, x0:x1]
        w,h,d = ball_area.shape
        ball_area = cv2.bitwise_and(ball_area, ball_area, mask=BALL_ROI[:w,:h])
        if self._is_phantom(ball_area):
            ball.type = ball_mod.TYPE_PHANTOM
            return

        if self._is_black(ball_area):
            ball.type = ball_mod.TYPE_BLACK
            return

        ratio = self._get_white_ratio(ball_area)
        if ratio > 0.50:
            ball.type = ball_mod.TYPE_CUE
            return

        if ratio > 0.22:
            ball.type = ball_mod.TYPE_STRIPE
            return 

        ball.type = ball_mod.TYPE_SOLID

    def _is_phantom(self, ball_area):
        l,u = self.get_dominant_color_range()
        masked = cv2.inRange(ball_area, l, u)
        return np.count_nonzero(masked) / float(masked.size) > 0.20

    def _is_black(self, ball_area):
        masked = cv2.inRange(ball_area, (0,0,0), (180,256,40))
        return np.count_nonzero(masked) / float(masked.size) > 0.45

    def _get_white_ratio(self, ball_area):
        import uuid
        masked = cv2.inRange(ball_area, (0,0,100), (180,90,255))
        # plt.subplot(2,3,1)
        # plt.imshow(ball_area)
        # plt.draw()

        # plt.subplot(2,3,2)
        # plt.imshow(masked)
        # plt.draw()

        # plt.subplot(2,3,3)
        # rgb = cv2.cvtColor(ball_area, cv2.COLOR_HSV2RGB)
        # plt.imshow(rgb)
        # plt.draw()

        # blur = cv2.blur(ball_area, (3,3))
        # blur_masked = cv2.inRange(blur, (0,0,100), (180,90,255))
        # plt.subplot(2,3,4)
        # plt.imshow(blur)
        # plt.draw()

        # plt.subplot(2,3,5)
        # plt.imshow(blur_masked)
        # plt.draw()

        # plt.subplot(2,3,6)
        # blur_rgb = cv2.cvtColor(blur, cv2.COLOR_HSV2RGB)
        # plt.imshow(blur_rgb)
        # plt.draw()

        # plt.show(block=False)

        # cv2.imwrite('ball_area_masked-%s.png' % (uuid.uuid4(),), masked)
        # cv2.imwrite('ball_area_masked-%s.png' % (uuid.uuid4(),), ball_area)
        return np.count_nonzero(masked) / float(masked.size)

    def get_table(self):
        size = self.original.shape
        table = Table(size[0], size[1])
        if self._is_ball_in_hand():
            table.set_ball_in_hand(True)
            table.set_hand(self._hand_pos)

        circles = self.get_circles()
        for c in circles[0,:]:
            ball = ball_mod.Ball(
                    x=int(np.round(c[0])), 
                    y=int(np.round(c[1])), 
                    r=BALL_RADIUS)
            if table.does_collide(ball):
                continue

            self._update_ball_detail(ball, table)
            if ball.type == ball_mod.TYPE_PHANTOM:
                continue

            # if ball-in-hand, then make sure cue ball is right under the hand
            # else it is a false positive match
            if ball.type == ball_mod.TYPE_CUE and table.is_ball_in_hand():
                x,y = table.get_hand()
                d = ((x-ball.x)**2 + (y-ball.y)**2)**0.5
                if d > BALL_RADIUS:
                    continue

            table.add_ball(ball)

        if self.debug:
            colored = self.original.copy()
            for b in table.get_balls():
                if b.type == ball_mod.TYPE_CUE or b.type == ball_mod.TYPE_BLACK:
                    color = (0,0,255) # red
                elif b.type == ball_mod.TYPE_STRIPE:
                    color = (0,255,0) # green
                elif b.type == ball_mod.TYPE_SOLID:
                    color = (0,255,255) # yellow

                cv2.circle(colored,(b.x, b.y), b.r,color,2)
                cv2.circle(colored,(b.x, b.y),2,(0,0,255),3)

            colored = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)
            plt.subplot(2,1,1)
            plt.imshow(colored)
            plt.draw()

            self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
            plt.subplot(2,1,2)
            plt.imshow(self.original)
            plt.draw()
            plt.show(block=False)
            # plt.show(block=True)

        return table

