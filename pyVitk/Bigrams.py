# coding=UTF-8

from pynlpl.lm import lm

class Bigrams(object):
    def __init__(self, bigramARPAFilname: str):
        self.bigrams = lm.ARPALanguageModel(bigramARPAFilname, base_e=False)

    def logProb(self, a: str):
        """
        Computes log(P(a)) in base 10.
        :param a: 
        :return: log(P(a)) in base 10.
        """
        t = None
        try:
            t = self.bigrams.ngrams.prob(tuple([a]))
        except KeyError:
            t = self.bigrams.ngrams.prob(tuple(['<unk>']))

        return t

    def logConditionalProb(self, a: str, b: str) -> float:
        """
        Computes log(P(b | a)) in base 10.
        :param a: 
        :param b: 
        :return: log(P(b | a)) in base 10.
        """
        t = (a, b)

        try:
            p = self.bigrams.ngrams.prob(t)
            return p
        except KeyError:
            x = self.logProb(b)

        try:
            py = self.bigrams.ngrams.backoff(tuple([a]))
        except KeyError:
            py = None

        if py != None:
            x += py  # add the backoff weight (log_{10})
        return x