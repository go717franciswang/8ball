import unittest
from pb.game_reader import GameReader, ItemNotFound
import cv2

class TestGameReader(unittest.TestCase):
    def setUp(self):
        self.g = GameReader()

    def testGetLocationFromImg(self):
        img = cv2.imread('resources/menu.jpg', 0)
        x, y = self.g._get_location_from_img(img, '8ball logo')
        self.assertTrue(x > 0)
        self.assertTrue(y > 0)

    def testGetLocationExceptionNotFound(self):
        img = cv2.imread('resources/sydney.jpg', 0)
        self.assertRaises(ItemNotFound, lambda: self.g._get_location_from_img(img, '8ball logo'))

    def testGetPlayerStatusYourTurn(self):
        img = cv2.imread('resources/player-status-your-turn.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, self.g.YOUR_TURN)

        img = cv2.imread('resources/player-status-your-turn2.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, self.g.YOUR_TURN)

