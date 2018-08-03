# coding=UTF-8

from unittest import TestCase
import logging
from pyVitk.test.helper import setup_logging
from pyVitk.Tokenizer import Tokenizer, PhraseGraph, PhraseGraph2, SegmentationFunction

# setup the logger
setup_logging()
logger = logging.getLogger(__name__)


class TokenzierTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug('Start TokenizerTest')
        cls.tokenizer = Tokenizer()

    @classmethod
    def tearDownClass(cls):
        cls.tokenizer = None
        cls.userTokenizer = None
        logger.debug('End TokenizerTest')

    def test_phrase_graph_1(self):
        graph = PhraseGraph(self.tokenizer)
        graph2 = PhraseGraph2(self.tokenizer)

        s = 'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia'

        logger.debug('testing shortest path of string: ' + s)

        # PhraseGraph
        graph.makeGraph(s)
        logger.debug('Graph Making Result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Graph Shortest paths Result: {}'.format(p))

        # PhraseGraph2
        graph2.makeGraph(s)
        logger.debug('Graph2 Making Result: {}'.format(graph2))

        p = graph2.shortestPath()
        logger.debug('Graph2 Shortest paths Result: {}'.format(p))
        "hay là một tổ_chức quốc_tế hoạt_động phi lợi_nhuận phi_chính_phủ và bao_gồm các thành_viên có trình_độ"

    def test_phrase_graph_2(self):
        graph = PhraseGraph(self.tokenizer)
        graph2 = PhraseGraph2(self.tokenizer)

        s = 'là phiên bản tiếng'

        logger.debug('testing shortest path of string: ' + s)

        #graph
        graph.makeGraph(s)
        logger.debug('Graph making result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Graph Shortest Paths: {}'.format(p))

        #graph2
        graph2.makeGraph(s)
        logger.debug('Graph2 making result: {}'.format(graph2))

        p = graph2.shortestPath()
        logger.debug('Graph2 Shortest Paths: {}'.format(p))

    def test_phrase_graph_3(self):
        graph = PhraseGraph(self.tokenizer)
        graph2 = PhraseGraph2(self.tokenizer)

        s = 'gần đây nhất mình thi'

        logger.debug('testing shortest path of string: ' + s)

        graph.makeGraph(s)
        logger.debug('Graph making result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Shortest Paths: {}'.format(p))

        # graph 2
        graph2.makeGraph(s)
        logger.debug('Graph2 making result: {}'.format(graph2))

        p = graph2.shortestPath()
        logger.debug('Shortest Paths: {}'.format(p))

    def test_tokenize_phrase(self):
        s = 'là phiên bản tiếng Việt'
        seg = SegmentationFunction(self.tokenizer)

        lst = seg.tokenizePhrase(s)
        logger.debug('Tokenized Phrase: {}'.format(lst))

    def test_tokenize_line(self):
        s = 'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia.'
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line2(self):
        s = 'Website được kích hoạt lần đầu tiên vào tháng 11 năm 2002, lúc đó chỉ có bài viết đầu tiên của dự án là bài Internet Society.[1] '
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenzie_line3(self):
        s = 'Vì dự án không có đủ người đóng góp, Wikipedia tiếng Việt không có thêm bài viết nào cho đến tháng 10 năm 2003 khi Trang Chính được viết,[2] và dự án Wikipedia tiếng Việt được xem như "khởi động lại nữa".'
        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenzie_line4(self):
        s = 'là ngôn ngữ có nguồn gốc bản địa'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line5(self):
        s = 'bắt đi bộ thế này'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line6(self):
        s = 'nhỏ*'

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line7(self):
        s = "gần đây nhất mình thi"

        t = self.tokenizer.tokenizeLine(s)

        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_tokenize_line8(self):
        s = '• Con gái của ba hả.↵• Dạ con chào ba.'
        t = self.tokenizer.tokenizeLine(s)
        logger.debug('Test tokenizeline, s: ' + s)
        logger.debug('Tokenized Result: {}'.format(t))

    def test_serialize_to_xml(self):
        self.tokenizer.to_lexicon_xml_file('test.xml')
