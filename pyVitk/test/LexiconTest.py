import unittest
import pyVitk.Lexicon as Lexicon


class LexiconTestCase(unittest.TestCase):
    def setUp(self):
        self.lexicon = Lexicon.Lexicon()
        self.lexicon.load('../dat/tok/lexicon.xml')
    def tearDown(self):
        self.lexicon = None

    def test_has_word(self):
        r = self.lexicon.hasWord('ai hoài')
        self.assertTrue(r)

        r = self.lexicon.hasWord('ngoại bang')
        self.assertTrue(r)

        r = self.lexicon.hasWord('ngoại giao nhân dân')
        self.assertTrue(r)

        r = self.lexicon.hasWord('dự án')
        self.assertTrue(r)

        r = self.lexicon.hasWord('phiên bản')
        self.assertTrue(r)

        r = self.lexicon.hasWord('ai Hoài')
        self.assertFalse(r)

        r = self.lexicon.hasWord('tiếng việt')
        self.assertFalse(r)
