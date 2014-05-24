import cv2
import numpy as np

class GameReader:
    def __init__(self):
        pass

    def get_game_state(self, img):
        """docstring for get_game"""
        pass

    def get_logo_location(self, img):
        """should only be ran when at the menu"""
        template = cv2.imread('resources/8ball-logo.jpg', 0)
        w, h = template.shape[::-1]

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(img, template, method)
        threshold = 0.95
        loc = np.where(res >= threshold)
        rs = zip(*loc)
        if len(rs) == 0:
            raise ItemNotFound

        top_left = rs[0]
        return top_left[0], top_left[1], w, h

class ItemNotFound(Exception):
    pass
    
