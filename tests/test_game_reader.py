import unittest
from pb.game_reader import GameReader, ItemNotFound
import cv2

class TestGameReader(unittest.TestCase):
    def setUp(self):
        self.g = GameReader()

    def testGetLogoLocation(self):
        img = cv2.imread('resources/menu.jpg', 0)
        x, y, w, h = self.g.get_logo_location(img)
        self.assertTrue(x > 0)
        self.assertTrue(y > 0)
        self.assertTrue(w > 0)
        self.assertTrue(h > 0)

    def testGetLogoLocationExceptionNotFound(self):
        img = cv2.imread('resources/sydney.jpg', 0)
        self.assertRaises(ItemNotFound, lambda: self.g.get_logo_location(img))
