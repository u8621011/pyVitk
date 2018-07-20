# encoding=utf-8

from unittest import TestCase
from pyVitk.crawler.VDictParser import parse_vdict
import json
import logging

# setup the logger
logger = logging.getLogger(__name__)
if not len(logger.handlers):
    # file handler
    hdlr = logging.FileHandler('unittest.log', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

class VDictParserTest(TestCase):
    def test_parse_vdict(self):
        results = parse_vdict('zh-TW', 'vi-VN', '要')
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 2)

        results = parse_vdict('zh-TW', 'vi-VN', '喝')
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 1)

        results = parse_vdict('zh-TW', 'vi-VN', '和')
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 2)
