import time
import unittest


class TestA(unittest.TestCase):
    def test_1(self):
        time.sleep(1)
        print("我是test_1")

    def test_2(self):
        time.sleep(1)
        print("我是test_2")
        assert 1==0

    def test_3(self):
        time.sleep(1)
        print("我是test_3")
