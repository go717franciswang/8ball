import unittest
import pb.screenshot 
import numpy as np

class TestScreenshot(unittest.TestCase):
    def testGetScreen(self):
        img = pb.screenshot.get_screenshot()
        isinstance(img, np.ndarray)

