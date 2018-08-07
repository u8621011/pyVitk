from unittest import TestCase
from pyVitk.crawler.ThiVienParser import parse_hanviet

class ThiVienParserTest(TestCase):
    def test_parse_from_tchinese(self):
        lexs = parse_hanviet('文')

        self.assertEqual(len(lexs), 1)
        self.assertEqual(lexs[0].source_language, 'zh-TW')
        self.assertEqual(lexs[0].target_language, 'vi-VN')
        self.assertEqual(lexs[0].source_title, '文')
        self.assertEqual(len(lexs[0].pron_systems), 2)

