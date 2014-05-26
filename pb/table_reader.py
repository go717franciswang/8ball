import cv2
import numpy as np

class TableReader:
    def __init__(self, img):
        """docstring for __init__"""
        pass

    def get_table(self):
        """docstring for get_table"""
        pass

if __name__ == '__main__':
    # convert image to HSV
    # use masking to get rid of background color
    # make everything else the same color
    # use Hough circle transform to detect the balls
    '''hough circle transform'''
    '''
    img = cv2.imread('resources/table1.jpg',0)
    cimg = cv2.imread('resources/table1.jpg',1)
    img = cv2.medianBlur(img,5)

    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)
    print circles

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    
    '''watershed
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_watershed/py_watershed.html'''
    from matplotlib import pyplot as plt

    img = cv2.imread('resources/table1.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    plt.imshow(thresh)
    plt.show()

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.cv.CV_DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0


