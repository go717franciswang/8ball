import cv2
import numpy as np
from matplotlib import pyplot as plt

class TableReader:
    def __init__(self, img):
        self.original = img.copy()
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_dominant_color_range(self):
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
        return map(tuple,bounds)

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

    def get_gray_img_no_background(self):
        masked = self.get_masked_black()
        # masked = cv2.medianBlur(masked,3)
        # masked = cv2.blur(masked,(3,3))
        masked_inv = cv2.bitwise_not(masked)

        img2 = cv2.bitwise_not(self.gray, mask=masked_inv)
        # plt.imshow(img2)
        # plt.show()
        return self._get_circles(img2)

    def _get_circles(self, img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.blur(img, (4,4))
        # img = cv2.medianBlur(img,3)
        circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,5, 
                param1=100,param2=10,minRadius=6,maxRadius=10)
        # print circles

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(self.original,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(self.original,(i[0],i[1]),2,(0,0,255),3)

        self.original = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        plt.imshow(self.original)
        plt.show()
        return circles

    def get_table(self):
        """docstring for get_table"""
        pass

if __name__ == '__main__':
    for i in xrange(1,5):
        img = cv2.imread('resources/table%d.jpg' % (i,))
        table = TableReader(img)
        table.get_gray_img_no_background()

