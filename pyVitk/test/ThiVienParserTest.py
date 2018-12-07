import logging
from unittest import TestCase
from pyVitk.crawler.ThiVienParser import parse_hanviet, parse_hanviet_from_vn
from pyVitk import helper

helper.setup_logging()
logger = logging.getLogger('unittest')

class ThiVienParserTest(TestCase):
    def test_parse_from_tchinese(self):
        lexs = parse_hanviet('文')

        self.assertEqual(len(lexs), 1)
        self.assertEqual(lexs[0].source_language, 'zh-TW')
        self.assertEqual(lexs[0].target_language, 'vi-VN')
        self.assertEqual(lexs[0].source_title, '文')
        self.assertEqual(len(lexs[0].pron_systems), 2)

    def test_parse_hanviet_from_vn(self):
        lexs = parse_hanviet_from_vn('ẩm')
        self.assertEqual(len(lexs), 2)
