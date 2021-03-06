import unittest
from pb.game_reader import GameReader, ItemNotFound, PS_YOUR_TURN, PS_OTHER
import pb.ball
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
        img = cv2.imread('resources/player_status-your-turn.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, PS_YOUR_TURN)

        img = cv2.imread('resources/player_status-your-turn2.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, PS_YOUR_TURN)

    def testGetPlayerStatusOther(self):
        img = cv2.imread('resources/player_status-opponent-turn.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, PS_OTHER)

        img = cv2.imread('resources/player_status-ball-rolling.jpg')
        status = self.g._get_player_status_from_img(img)
        self.assertEquals(status, PS_OTHER)

    def testGetTargetFromImg(self):
        img = cv2.imread('resources/ball-target-black.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_BLACK)

        img = cv2.imread('resources/ball-target-nothing.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, None)

        img = cv2.imread('resources/ball-target-stripe1.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_STRIPE)

        img = cv2.imread('resources/ball-target-stripe2.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_STRIPE)

        img = cv2.imread('resources/ball-target-stripe3.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_STRIPE)

        img = cv2.imread('resources/ball-target-solid1.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_SOLID)

        img = cv2.imread('resources/ball-target-solid2.jpg')
        target = self.g._get_target_from_img(img)
        self.assertEquals(target, pb.ball.TYPE_SOLID)
