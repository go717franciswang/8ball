import cv2
import numpy as np
from matplotlib import pyplot as plt
from position import get_position
from screenshot import get_screenshot

resources = {
        '8ball logo': 'resources/8ball-logo.jpg',
        'vegas logo': 'resources/vegas-logo.jpg',
        'tokyo logo': 'resources/tokyo-logo.jpg',
        'moscow logo': 'resources/moscow-logo.jpg',
        'sydney logo': 'resources/sydney-logo.jpg',
        'london logo': 'resources/london-logo.jpg',
        'kasbah logo': 'resources/kasbah-logo.jpg',
        'toronto logo': 'resources/toronto-logo.jpg',
        'jakarta logo': 'resources/jakarta-logo.jpg',
        }

class GameReader:
    YOUR_TURN = 1
    OPPONENT_TURN = 2
    BALL_ROLLING = 3

    def __init__(self, debug=False):
        self._debug = debug
        self._locations = {}

    def get_game_state(self, img):
        """docstring for get_game"""
        pass

    def get_location_from_entire_screen(self, search_item):
        img = get_screenshot()
        pos = self._get_location_from_img(img, search_item)
        self._locations[search_item] = pos
        return pos

    def get_location_from_game(self, search_item, game_top_left_position=None):
        a = game_top_left_position
        if game_top_left_position is None:
            a = get_position('8ball logo', self._locations['8ball logo'], 'game top left')
        b = get_position('game top left', a, 'game bottom right')
        w = b[0]-a[0]
        h = b[1]-a[1]
        x,y = a
        img = get_screenshot(x,y,w,h)
        return self._get_location_from_img(img, search_item, a[0], a[1])

    def _get_location_from_img(self, img, search_item, dx=0, dy=0):
        if self._debug:
            plt.imshow(img,cmap='gray')
            plt.draw()
            plt.show(block=False)

        resource = resources[search_item]
        template = cv2.imread(resource, 0)
        w,h = template.shape[::-1]

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(img, template, method)
        threshold = 0.95
        loc = np.where(res >= threshold)
        rs = zip(*loc)
        if len(rs) == 0:
            raise ItemNotFound

        top_left = rs[0]
        return top_left[1]+w/2+dx, top_left[0]+h/2+dy

    def get_player_status(self):
        a = get_position('logo', self._locations['8ball logo'], 'player status top left')
        b = get_position('player status top left', a, 'player status bottom right')
        w = b[0]-a[0]
        h = b[1]-a[1]
        x,y = a
        img = get_screenshot(x,y,w,h,grayscale=False)
        if self._debug:
            # same the images for debug and write tests for different statuses
            import time
            cv2.imwrite('%d_player_status.jpg' % (time.time()*10000,), img)
            plt.imshow(img)
            plt.draw()
            plt.show(block=False)

    def _get_player_status_from_img(self, img):
        return 0

class ItemNotFound(Exception):
    pass
    
