# coding=UTF-8

import unittest
import pyVitk.Bigrams as Bigrams

class BigramsTestCase(unittest.TestCase):
    def setUp(self):
        self.bigrams = Bigrams.Bigrams('../dat/tok/syllables2M.arpa')

    def tearDown(self):
        self.bigrams = None

    def test_log_prob(self):
        s = 'cả nằm'
        p = self.bigrams.logProb(s)
        self.assertEqual(-1.132573, p)

        s = 'hổ'
        p = self.bigrams.logProb(s)
        self.assertEqual(p, -4.658729)

    def test_log_conditional_prob(self):
        # case of not found of all, but found first and last one.
        s = 'chân mẫu'  # backoff(s[0]) = -0.2912827, s[1] = -3.652592, p = -3.9438747
        sp = s.split()
        p = self.bigrams.logConditionalProb(sp[0], sp[1])
        self.assertEqual(-3.9438747, p)

        # case of not found of all, only found the last word
        s = 'khán1 khám'  # backoff(s[0]) = None, s[1] = -3.746877, p = -3.746877
        sp = s.split()
        p = self.bigrams.logConditionalProb(sp[0], sp[1])
        self.assertEqual(-3.746877, p)

        # case of found of all
        s = 'kho chứa'
        sp = s.split()
        p = self.bigrams.logConditionalProb(sp[0], sp[1])
        self.assertEqual(-1.394299, p)