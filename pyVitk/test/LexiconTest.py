# encoding=utf-8

import unittest
import pyVitk.Lexicon as Lexicon


class LexiconTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_has_word_sensitive(self):
        lexicon = Lexicon.Lexicon(case_sensitive=True)
        r = lexicon.hasWord('ai hoài')
        self.assertTrue(r)

        r = lexicon.hasWord('ngoại bang')
        self.assertTrue(r)

        r = lexicon.hasWord('ngoại giao nhân dân')
        self.assertTrue(r)

        r = lexicon.hasWord('dự án')
        self.assertTrue(r)

        r = lexicon.hasWord('Dự án')
        self.assertFalse(r)

        r = lexicon.hasWord('phiên bản')
        self.assertTrue(r)

        r = lexicon.hasWord('ai hoài')
        self.assertTrue(r)

        r = lexicon.hasWord('ai Hoài')
        self.assertFalse(r)

        r = lexicon.hasWord('tiếng việt')
        self.assertFalse(r)

    def test_has_word_insensitive(self):
        lexicon = Lexicon.Lexicon(case_sensitive=False)
        r = lexicon.hasWord('ai hoài')
        self.assertTrue(r)

        r = lexicon.hasWord('ngoại bang')
        self.assertTrue(r)

        r = lexicon.hasWord('ngoại giao nhân dân')
        self.assertTrue(r)

        r = lexicon.hasWord('dự án')
        self.assertTrue(r)

        r = lexicon.hasWord('Dự án')
        self.assertTrue(r)

        r = lexicon.hasWord('phiên bản')
        self.assertTrue(r)

        r = lexicon.hasWord('ai hoài')
        self.assertTrue(r)

        r = lexicon.hasWord('ai Hoài')
        self.assertTrue(r)

        r = lexicon.hasWord('tiếng việt')
        self.assertFalse(r)