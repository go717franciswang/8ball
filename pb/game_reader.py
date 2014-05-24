import cv2
import numpy as np
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
    def __init__(self):
        pass

    def get_game_state(self, img):
        """docstring for get_game"""
        pass

    def get_location_from_entire_screen(self, search_item):
        img = get_screenshot()
        return self._get_location_from_img(img, search_item)

    def get_location_from_game(self, search_item, game_top_left_position):
        a = game_top_left_position
        b = get_position('game top left', a, 'game bottom right')
        w = b[1]-a[1]
        h = b[0]-a[0]
        x,y = a
        img = get_screenshot(x,y,w,h)
        return self._get_location_from_img(img, search_item, a[0], a[1])

    def _get_location_from_img(self, img, search_item, x_offset=0, y_offset=0):
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
        return top_left[1]+w/2, top_left[0]+h/2

class ItemNotFound(Exception):
    pass
    
