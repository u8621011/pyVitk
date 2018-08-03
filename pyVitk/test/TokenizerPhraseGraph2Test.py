# coding=UTF-8
import unittest
import logging
from pyVitk.test.helper import setup_logging
from pyVitk.Tokenizer import PhraseGraph2, Tokenizer
from pyVitk.Bigrams import Bigrams

# setup the logger
setup_logging()
logger = logging.getLogger(__name__)


class TokenzierPhraseGraph2TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()
        cls.bigram = Bigrams('../dat/tok/syllables2M.arpa')

    @classmethod
    def tearDownClass(cls):
        cls.tokenizer = None
        cls.bigram = None

    def test_user_toenzie_line1(self):
        phrase = PhraseGraph2(self.tokenizer, self.bigram)
        s = "người tha hương"

        phrase.makeGraph(s)

        path = phrase.shortestPath()
        logger.debug('path of "{}": {}'.format(s, path))

        words = phrase.get_words()
        logger.debug('segmented words: {}'.format(words))


    def test_user_toenzie_line2(self):
        phrase = PhraseGraph2(self.tokenizer, self.bigram)
        s = "người tha hương người"

        phrase.makeGraph(s)

        path = phrase.shortestPath()
        logger.debug('path of "{}": {}'.format(s, path))

        words = phrase.get_words()
        logger.debug('segmented words: {}'.format(words))

    def test_user_toenzie_line3(self):
        phrase = PhraseGraph2(self.tokenizer, self.bigram)
        s = "người tha hương người người quyết tâm"

        phrase.makeGraph(s)

        path = phrase.shortestPath()
        logger.debug('path of "{}": {}'.format(s, path))

        words = phrase.get_words()
        logger.debug('segmented words: {}'.format(words))

    def test_user_toenzie_line4(self):
        phrase = PhraseGraph2(self.tokenizer, self.bigram)
        s = "người tha hương người người  người quyết tâm"

        phrase.makeGraph(s)

        path = phrase.shortestPath()
        logger.debug('path of "{}": {}'.format(s, path))

        words = phrase.get_words()
        logger.debug('segmented words: {}'.format(words))