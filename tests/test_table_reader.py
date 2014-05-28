import unittest
from pb.table_reader import TableReader
from pb.table import Table
import cv2

class TestTableReader(unittest.TestCase):
    def testTableReturnsATable(self):
        img = cv2.imread('resources/table1.jpg')
        table = TableReader(img).get_table()
        self.assertTrue(isinstance(table, Table))

    def testIsBallInHandTrue(self):
        img = cv2.imread('resources/table1.jpg')
        table = TableReader(img).get_table()
        self.assertTrue(table.is_ball_in_hand())

        hand_pos = table.get_hand()
        expected = (142, 141) # from eyeballing @_@
        self.assertAlmostEqual(hand_pos[0], expected[0], delta=3)
        self.assertAlmostEqual(hand_pos[1], expected[1], delta=3)

    def testIsBallInHandFalse(self):
        img = cv2.imread('resources/table2.jpg')
        table = TableReader(img).get_table()
        self.assertFalse(table.is_ball_in_hand())

    def testCorrectNumberOfBalls(self):
        # phantom ball is excluded
        expected_ball_count = {
                'resources/table1.jpg': 16,
                'resources/table2.jpg': 14,
                'resources/table3.jpg': 12,
                'resources/table4.jpg': 7,
                }

        for img_path, expected_count in expected_ball_count.items():
            img = cv2.imread(img_path)
            table = TableReader(img, debug=True).get_table()
            self.assertEquals(len(table.get_balls()), expected_count)


