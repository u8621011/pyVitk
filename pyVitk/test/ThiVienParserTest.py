from unittest import TestCase
from pyVitk.crawler.ThiVienParser import parse_hanviet

class ThiVienParserTest(TestCase):
    def test_parse_from_tchinese(self):
        hanviets = parse_hanviet('文')
        self.assertEqual(len(hanviets), 2)
