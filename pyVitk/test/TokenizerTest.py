# coding=UTF-8

from unittest import TestCase
import logging
from pyVitk.helper import setup_logging
from pyVitk.Tokenizer import Tokenizer, PhraseGraph, SegmentationFunction

# setup the logger
setup_logging()
logger = logging.getLogger(__name__)


class TokenzierTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug('Start TokenizerTest')
        cls.tokenizer = Tokenizer(case_sensitive=True)
        cls.tokenizer_insensitive = Tokenizer(case_sensitive=False)

    @classmethod
    def tearDownClass(cls):
        cls.tokenizer = None
        cls.userTokenizer = None
        logger.debug('End TokenizerTest')

    def assert_expected_tokens(self, tokens, expections):
        for t, e in zip(tokens, expections):
            self.assertEqual(t.text, e)

    def test_phrase_graph_1(self):
        graph = PhraseGraph(self.tokenizer)

        s = 'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia'

        logger.debug('testing shortest path of string: ' + s)

        # PhraseGraph
        graph.makeGraph(s)
        logger.debug('Graph Making Result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Graph Shortest paths Result: {}'.format(p))

    def test_phrase_graph_2(self):
        graph = PhraseGraph(self.tokenizer)

        s = 'là phiên bản tiếng'

        logger.debug('testing shortest path of string: ' + s)

        #graph
        graph.makeGraph(s)
        logger.debug('Graph making result: {}'.format(graph))

        p = graph.shortestPaths()
        logger.debug('Graph Shortest Paths: {}'.format(p))


    def test_phrase_graph_3(self):
        graph = PhraseGraph(self.tokenizer)

        s = 'gần đây nhất mình thi'

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
        lines = [
            'là ngôn ngữ có nguồn gốc bản địa',
            'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia.',
            'Website được kích hoạt lần đầu tiên vào tháng 11 năm 2002, lúc đó chỉ có bài viết đầu tiên của dự án là bài Internet Society.[1] ',
            'Vì dự án không có đủ người đóng góp, Wikipedia tiếng Việt không có thêm bài viết nào cho đến tháng 10 năm 2003 khi Trang Chính được viết,[2] và dự án Wikipedia tiếng Việt được xem như "khởi động lại nữa".',
            'bắt đi bộ thế này',
            'nhỏ*',
            'gần đây nhất mình thi',
            '• Con gái của ba hả.↵• Dạ con chào ba.',
            'Tiết độ sứ Tiết tiếu lâm tiềm Lực.',
            'PHD | Xem Đi Xem Lại Cả 1000 Lần Mà Vẫn Không Thể Nhịn Được Cười | Funny Videos,',
            'BÍCH PHƯƠNG - Bao Giờ Lấy Chồng? [OFFICIAL M/V]',
            'Kem Xôi TV: Tập 74 - Dài bao nhiêu là đủ,',
        ]
        expected = [
            ['là',  'ngôn ngữ',  'có',  'nguồn gốc', 'bản địa'],
            ['Wikipedia', 'tiếng', 'Việt', 'là', 'phiên bản', 'tiếng', 'Việt', 'của', 'dự án', 'Wikipedia', '.'],
            ['Website', 'được', 'kích hoạt', 'lần', 'đầu tiên', 'vào', 'tháng', '11', 'năm', '2002', ',', 'lúc', 'đó', 'chỉ', 'có', 'bài', 'viết', 'đầu tiên', 'của', 'dự án', 'là', 'bài', 'Internet', 'Society', '.', '[', '1', ']'],
            ['Vì', 'dự án', 'không', 'có', 'đủ', 'người', 'đóng góp', ',', 'Wikipedia', 'tiếng', 'Việt', 'không', 'có', 'thêm', 'bài', 'viết', 'nào', 'cho', 'đến', 'tháng', '10', 'năm', '2003', 'khi', 'Trang', 'Chính', 'được', 'viết', ',', '[', '2', ']', 'và', 'dự án', 'Wikipedia', 'tiếng', 'Việt', 'được', 'xem', 'như', '"', 'khởi động', 'lại', 'nữa', '".'],
            ['bắt', 'đi', 'bộ', 'thế', 'này'],
            ['nhỏ', '*'],
            ['gần', 'đây', 'nhất', 'mình', 'thi'],
            ['•', 'Con', 'gái', 'của', 'ba', 'hả', '.', '↵', '•', 'Dạ', 'con', 'chào', 'ba', '.'],
            ['Tiết', 'độ', 'sứ', 'Tiết', 'tiếu lâm', 'tiềm', 'Lực', '.'],
            ['PHD', '|', 'Xem', 'Đi', 'Xem', 'Lại', 'Cả', '1000', 'Lần', 'Mà', 'Vẫn', 'Không', 'Thể', 'Nhịn', 'Được', 'Cười', '|', 'Funny', 'Videos', ','],
            ['BÍCH', 'PHƯƠNG', '-', 'Bao', 'Giờ', 'Lấy', 'Chồng', '?', '[', 'OFFICIAL', 'M/V', ']', ],
            ['Kem', 'Xôi', 'TV', ':', 'Tập', '74', '-', 'Dài', 'bao nhiêu', 'là', 'đủ', ',']
        ]

        for s, e in zip(lines, expected):
            t = self.tokenizer.tokenizeLine(s)
            self.assert_expected_tokens(t, e)

    def test_tokenize_line_concat(self):
        lines = [
            'là ngôn ngữ có nguồn gốc bản địa',
            'Wikipedia tiếng Việt là phiên bản tiếng Việt của dự án Wikipedia.',
            'Website được kích hoạt lần đầu tiên vào tháng 11 năm 2002, lúc đó chỉ có bài viết đầu tiên của dự án là bài Internet Society.[1] ',
            'Vì dự án không có đủ người đóng góp, Wikipedia tiếng Việt không có thêm bài viết nào cho đến tháng 10 năm 2003 khi Trang Chính được viết,[2] và dự án Wikipedia tiếng Việt được xem như "khởi động lại nữa".',
            'bắt đi bộ thế này',
            'nhỏ*',
            'gần đây nhất mình thi',
            '• Con gái của ba hả.↵• Dạ con chào ba.',
            'Tiết độ sứ Tiết tiếu lâm tiềm Lực.',
            'PHD | Xem Đi Xem Lại Cả 1000 Lần Mà Vẫn Không Thể Nhịn Được Cười | Funny Videos,',
            'BÍCH PHƯƠNG - Bao Giờ Lấy Chồng? [OFFICIAL M/V]',
            'Kem Xôi TV: Tập 74 - Dài bao nhiêu là đủ,',
        ]
        expected = [
            ['là',  'ngôn_ngữ',  'có',  'nguồn_gốc', 'bản_địa'],
            ['Wikipedia', 'tiếng', 'Việt', 'là', 'phiên_bản', 'tiếng', 'Việt', 'của', 'dự_án', 'Wikipedia', '.'],
            ['Website', 'được', 'kích_hoạt', 'lần', 'đầu_tiên', 'vào', 'tháng', '11', 'năm', '2002', ',', 'lúc', 'đó', 'chỉ', 'có', 'bài', 'viết', 'đầu_tiên', 'của', 'dự_án', 'là', 'bài', 'Internet', 'Society', '.', '[', '1', ']'],
            ['Vì', 'dự_án', 'không', 'có', 'đủ', 'người', 'đóng_góp', ',', 'Wikipedia', 'tiếng', 'Việt', 'không', 'có', 'thêm', 'bài', 'viết', 'nào', 'cho', 'đến', 'tháng', '10', 'năm', '2003', 'khi', 'Trang', 'Chính', 'được', 'viết', ',', '[', '2', ']', 'và', 'dự_án', 'Wikipedia', 'tiếng', 'Việt', 'được', 'xem', 'như', '"', 'khởi_động', 'lại', 'nữa', '".'],
            ['bắt', 'đi', 'bộ', 'thế', 'này'],
            ['nhỏ', '*'],
            ['gần', 'đây', 'nhất', 'mình', 'thi'],
            ['•', 'Con', 'gái', 'của', 'ba', 'hả', '.', '↵', '•', 'Dạ', 'con', 'chào', 'ba', '.'],
            ['Tiết', 'độ', 'sứ', 'Tiết', 'tiếu_lâm', 'tiềm', 'Lực', '.'],
            ['PHD', '|', 'Xem', 'Đi', 'Xem', 'Lại', 'Cả', '1000', 'Lần', 'Mà', 'Vẫn', 'Không', 'Thể', 'Nhịn', 'Được', 'Cười', '|', 'Funny', 'Videos', ','],
            ['BÍCH', 'PHƯƠNG', '-', 'Bao', 'Giờ', 'Lấy', 'Chồng', '?', '[', 'OFFICIAL', 'M/V', ']', ],
            ['Kem', 'Xôi', 'TV', ':', 'Tập', '74', '-', 'Dài', 'bao_nhiêu', 'là', 'đủ', ',']
        ]

        for s, e in zip(lines, expected):
            t = self.tokenizer.tokenizeLine(s, concat=True)
            self.assert_expected_tokens(t, e)

    def test_serialize_to_xml(self):
        self.tokenizer.to_lexicon_xml_file('test.xml')
