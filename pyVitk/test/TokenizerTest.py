# coding=UTF-8

import unittest
import logging
from pyVitk.Tokenizer import Tokenizer, PhraseGraph, SegmentationFunction

# setup the logger
logger = logging.getLogger(__name__)
if not len(logger.handlers):
    # file handler
    hdlr = logging.FileHandler('unittest.log', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)

class TokenzierTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()

    @classmethod
    def tearDownClass(cls):
        cls.tokenizer = None
        cls.userTokenizer = None

    def test_make_graph(self):
        graph = PhraseGraph(self.tokenizer)

        graph.makeGraph('Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia')

        logger.debug('Graph Making Result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Shortest paths Result: {}'.format(p))

    def test_shortest_paths(self):
        graph = PhraseGraph(self.tokenizer)

        s = 'là phiên bản tiếng'

        logger.debug('testing shortest path of string: ' + s)

        graph.makeGraph(s)
        logger.debug('Graph making result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Shortest Paths: {}'.format(p))

    def test_tokenize_phrase(self):
        s = 'là phiên bản tiếng Việt'
        seg = SegmentationFunction(self.tokenizer)

        lst = seg.tokenizePhrase(s)
        logger.debug('Tokenized Phrase: {}'.format(lst))

    def test_tokenize_line(self):
        s = 'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia.'
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line2(self):
        s = 'Website được kích hoạt lần đầu tiên vào tháng 11 năm 2002, lúc đó chỉ có bài viết đầu tiên của dự án là bài Internet Society.[1] '
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenzie_line3(self):
        s = 'Vì dự án không có đủ người đóng góp, Wikipedia tiếng Việt không có thêm bài viết nào cho đến tháng 10 năm 2003 khi Trang Chính được viết,[2] và dự án Wikipedia tiếng Việt được xem như "khởi động lại nữa".'
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenzie_line4(self):
        s = 'là ngôn ngữ có nguồn gốc bản địa'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line5(self):
        s = 'bắt đi bộ thế này'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line6(self):
        s = 'nhỏ*'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Tokenized Result: {}'.format(t))
