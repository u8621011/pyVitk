# encoding=utf-8

from unittest import TestCase
from pyVitk.crawler.VNY2KParser import parse_vny2k
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

class VNY2KParserTest(TestCase):
    def test_parse_vny2k(self):
        results = parse_vny2k('中文')
        logger.debug('parse result: %r', results)
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 1)

        results = parse_vny2k('句子')
        logger.debug('parse result: %r', results)
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 1)

        results = parse_vny2k('辭典')
        logger.debug('parse result: %r', results)
        for r in results:
            print(json.dumps(r.__dict__, ensure_ascii=False))
        self.assertEqual(len(results), 1)