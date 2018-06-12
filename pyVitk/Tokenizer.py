# coding=UTF-8

import sys
import regex
import logging
from typing import List
from .Lexicon import Lexicon
from .Bigrams import Bigrams
from .Dijkstra import Dijkstra
from .Dijkstra2 import Graph, shortest_path

logger = logging.getLogger('pyVitk.Tokenizer')


class PhraseGraph2(object):
    def __init__(self, tokenizer: 'Tokenizer', bigrams: 'Bigrams' = None):
        self.tokenizer = tokenizer
        self.bigrams = bigrams
        self.graph = Graph()
        self.syllables = None
        self.n = None

    def makeGraph(self, phrase: str):
        self.syllables = phrase.split()

        self.syllables.insert(0, '<s>')
        self.syllables.append('</s>')

        self.n = len(self.syllables)
        if self.n > 128:
            logger.info('Phrase too long (>= 128 syllables), tokenization may be slow...')
            logger.info(phrase)

        edge_count = [0] * self.n
        for i in range(1, self.n - 1):
            token_prob = token = self.syllables[i]
            for j in range(i, self.n - 1):
                if j > i + 10:
                    break   # we only process first 10th tokens.
                if self.tokenizer.lexicon.hasWord(token):     # can be segmented out
                    if self.bigrams:
                        self.graph.add_edge(i-1, j, self.bigrams.logConditionalProb(self.syllables[i-1], token),
                                            add_vertex=True)
                    else:
                        self.graph.add_edge(i-1, j, 1, add_vertex=True)
                    edge_count[j] = edge_count[j] + 1

                token = token + " " + self.syllables[j + 1]
                token_prob = token_prob + "_" + self.syllables[j + 1]

        # make sure that the graph is connected by adding adjacent edges if necessary
        for i in reversed(range(1, self.n)):
            if edge_count[i] == 0:  # i cannot reach by any previous node
                if self.bigrams:
                    self.graph.add_edge(i - 1, i, self.bigrams.logConditionalProb(self.syllables[i-1], self.syllables[i]),
                                        add_vertex=True)
                else:
                    self.graph.add_edge(i - 1, i, 1, add_vertex=True)

        logger.debug('"{}" makeGraph result : {}'.format(phrase, self.graph))

    def shortestPath(self) -> list:
        if self.bigrams:
            # find shortest path with maximum the possibility
            return shortest_path(self.graph, 0, self.n - 1, find_min=False)
        else:
            return shortest_path(self.graph, 0, self.n - 1)

    def get_words(self) -> list:
        lst_words = []

        start_node = None
        path = self.shortestPath()
        for stop_node in path:
            if start_node is not None:
                if stop_node == self.n - 1:
                    if start_node + 1 != stop_node:
                        words = ' '.join(self.syllables[start_node + 1: stop_node])
                        lst_words.append(words)
                else:
                    words = ' '.join(self.syllables[start_node + 1: stop_node + 1])
                    lst_words.append(words)

            start_node = stop_node

        return lst_words

class PhraseGraph(object):
    def __init__(self, tokenizer: 'Tokenizer'):
        self.tokenizer = tokenizer
        self.edges = {}
        self.syllables = []
        self.n = 0

    def makeGraph(self, phrase: str):
        """
        Build edges from input phrase. each edge is the place to save incoming edge of corresponding node.
        
        :param phrase: 
        :return: 
        """
        self.edges = {}
        self.syllables = phrase.split()
        self.n = len(self.syllables)

        if self.n > 128:
            logger.info('Phrase too long (>= 128 syllables), tokenization may be slow...')
            logger.info(phrase)

        # initialize the edges structure
        for j in range(self.n + 1):
            self.edges[j] = []

        for i in range(self.n):
            token = self.syllables[i]
            j = i
            while j < self.n:
                if self.tokenizer.lexicon.hasWord(token):
                    self.edges[j+1].append(i)
                j += 1
                if j < self.n:
                    token = token + ' ' + self.syllables[j]
        # make sure that the graph is connected by adding adjacent
        # edges if necessary
        for i in reversed(range(self.n)):
            if len(self.edges[i + 1]) == 0: # i cannot reach by any previous node
                self.edges[i + 1].append(i)
        logger.debug('Edges built: {}'.format(self.edges))

    def shortestPaths(self) -> list:
        """
        Finds all shortest paths from the first node to the last node of this graph. 
        :return: a list of paths, each path is a linked list of vertices.
        """
        dijkstra = Dijkstra(self.edges)
        allPaths = dijkstra.shortestPaths()

        return allPaths

    def words(self, path: list) -> list:
        """
        Gets a list of words specified by a given path.
        :param path: 
        :return: a list of words.
        """
        m = len(path)
        if m <= 1:
            return []
        a = path
        tok = []
        for j in range(m-1):
            # get the token from a[j] to a[j+1] (exclusive)
            i = a[j]
            lstSyllables = list()
            lstSyllables.append(self.syllables[i])
            for k in range(a[j] + 1, a[j + 1]):
                lstSyllables.append(' ')
                lstSyllables.append((self.syllables[k]))
            tok.append(lstSyllables)

        result = []
        for sb in tok:
            result.append(''.join(sb))

        return result

    def select(self, paths: list) -> int:
        """
        Selects the most likely segmentation from a list of different segmentations.
        :param paths: 
        :return: 
        """
        if  self.tokenizer.bigrams is not None:
            maxIdx = 0
            maxVal = float('-inf')

            # find the maximum of log probabilities of segmentations
            for j in range(len(paths)):
                path = paths[j]
                words = self.words(path)
                words.insert(0, '<s>')
                words.append('</s>')
                p = 0.0
                for w in range(1, len(words)):
                    p += self.tokenizer.bigrams.logConditionalProb(words[w - 1], words[w])
                if p > maxVal:
                    maxVal = p
                    maxIdx = j
            return maxIdx
        return 0

    def __str__(self):
        ptn = 'Syllables ({})\nEdges ({})'
        if not self.syllables:
            return ptn.format('Empty', 'Empty')

        return ptn.format(self.syllables, self.edges)


class SegmentationFunction(object):
    def __init__(self, tokenizer: 'Tokenizer'):
        self.tokenizer = tokenizer

    def segment(self, sentence: str) -> list:
        tokens = []

        sentence = sentence.strip()
        if len(sentence) == 0:
            return tokens

        s = sentence
        while True:
            maxLen = 0
            nextToken = None
            tokenType = None

            # greedy search for the longest pattern from the beginning of 's'
            logger.debug('Segmenting sentence: ' + s)
            for k, p in self.tokenizer.patterns.items():
                # return matchobject if matches
                m = p.match(s)
                if m:
                    logger.debug('【{}】 matched: {}'.format(s, k))
                    curLen = m.end(0) - m.start(0)
                    if maxLen < curLen:
                        maxLen = curLen
                        nextToken = m.group(0)
                        tokenType = k
                        nextToken = nextToken.strip()
                else:
                    #logger.debug('Test {} with pattern {}: not matched'.format(s, p))
                    pass

            if tokenType:
                logger.debug('longest matched pattern type: {}, token: {}'.format(tokenType, nextToken))
            else:
                logger.debug('Cannot find the matched pattern.')

            # split off the longest token we found.
            if nextToken:
                s = s[maxLen:].strip()
                # process the token we found
                if 'name' in tokenType and len(s) > 0:
                    tup = self.processName(nextToken, s)
                    if len(tup[0]) != len(nextToken):
                        nextToken = tup[0]
                        s = tup[1]
                        tokenType = 'word'

                    logger.debug('appending new token, type: {}, token: {}'.format(tokenType, nextToken))
                    tokens.append((tokenType, nextToken))
                elif 'unit' in tokenType and len(s) > 0:
                    tup = self.processUnit(nextToken, s)
                    if len(tup[0]) > len(nextToken):
                        nextToken = tup[0]
                        s = tup[1]
                        tokenType = "unit"

                    logger.debug('appending new token, type: {}, token: {}'.format(tokenType, nextToken))
                    tokens.append((tokenType, nextToken))
                elif 'phrase' in tokenType:
                    if nextToken.find(' ') > 0:    # multi-syllabic phrase
                        if  self.tokenizer.classifier is not None:
                            raise NotImplementedError
                        else:
                            # segment the phrase using a phrase graph
                            words = self.tokenizePhrase(nextToken)
                            #words = self.tokenizePhrase2(nextToken)
                            if words is not None:
                                for i in range(len(words)):
                                    logger.debug(
                                        'appending new token, type: {}, token: {}'.format(tokenType, words[i]))
                                    tokens.append(("word", words[i]))
                            else:
                                logger.info('Error when tokenizing phrase: ' + nextToken)
                    else:
                        logger.debug(
                            'appending new token, type: {}, token: {}'.format('word', nextToken))
                        tokens.append(("word", nextToken))
                else:
                    tokens.append((tokenType, nextToken))
            else:
                if len(s.strip()) > 0:
                    logger.warning('Unprocessed substring: ' + s)
                    break

            if len(s) == 0:
                break
        return tokens

    def processUnit(self, currentToken: str, s: str) -> (str, str):
        # "[đồng/đô] [la Mỹ...]" => [đồng/đô la] [Mỹ...]
        # "[đồng/cổ phiếu] [...]"
        lastSyllable = currentToken[currentToken.find('/') + 1]
        j = s.find(' ')
        if j > 0:
            nextSyllable = s[0: j]
        else:
            nextSyllable = s
        # s can either be "phiếu" or "phiếu.", find the last alphabetic character of s
        # so as to leave the non-alphabetic characters out.
        u = len (nextSyllable)
        for i in reversed(range(u)):
            if not nextSyllable[i].isalpha():
                u = i
                break
        nextSyllable = nextSyllable[0:u+1]

        if self.tokenizer.lexicon.hasWord(lastSyllable + ' ' + nextSyllable):
            currentToken = currentToken + ' ' + nextSyllable
            s = s[len(nextSyllable)].strip()
        return currentToken, s

    def processName(self, currentToken: str, s: str) -> (str, str):
        # If this is a name pattern, we process it further to capture 2 cases:
        # 1. It should be merged with the next syllable, like in "Thủ tướng" or "Bộ Giáo dục." where
        # the name pattern captures only the first part "Thủ" or "Bộ Giáo".
        # We try to combine the last syllable of the current token with the first token of s
        # to see whether they may form a word or not, note that the first token of s may contain
        # delimiters (like "dục." in the example above); we therefore need to remove them
        # beforehand if necessary.
        j = s.find(' ')
        if j > 0:
            nextSyllable = s[0:j]
        else:
            nextSyllable = ''

        # s can either be "dục" or "dục.", find the last alphabetic character of s
        # so as to leave the non-alphabetic characters out.
        u = len(nextSyllable)
        for i in reversed(range(u)):
            if not nextSyllable[i].isalpha():
                u = i
                break

        nextSyllable = nextSyllable[0:u+1]

        # find the following token
        k = currentToken.rfind(' ')
        if k > 0:
            lastSyllable = currentToken[k+1:]
            nextTokenPrefix = currentToken[0:k+1]
        else:
            lastSyllable = ''
            nextTokenPrefix = ''
        w = lastSyllable.lower() + ' ' + nextSyllable
        if self.tokenizer.lexicon.hasWord(w):
            currentToken = nextTokenPrefix + lastSyllable + ' ' + nextSyllable
            s = s[len(nextSyllable):].strip()

        # 2. It should be divided into two parts if the first syllable of the name
        # is a name prefix like "Ông", "Bà", "Anh", "Em", etc.
        j = currentToken.find(' ')
        if j > 0:
            firstSyllable = currentToken[0:j]
            matcher = self.tokenizer.patterns["prefix"].match(firstSyllable)
            if matcher:
                s = currentToken[j+1:] + ' ' + s
                currentToken = firstSyllable
        return currentToken, s

    def tokenizePhrase2(self, phrase: str) -> List[str]:
        """
        Tokenizes a phrase and use bigram to search the shorest path if bigram exist.
        :param phrase:
        :return:
        """
        self.tokenizer.graph2.makeGraph(phrase)
        return self.tokenizer.graph2.get_words()


    def tokenizePhrase(self, phrase: str)->List[str]:
        """
        Tokenizes a phrase.
        :param phrase: 
        :return: a list of tokens.
        """
        self.tokenizer.graph.makeGraph(phrase)
        paths = self.tokenizer.graph.shortestPaths()
        if len(paths) > 0:
            selectedPath = paths[len(paths) - 1]
            if self.tokenizer.bigrams is not None:
                best = self.tokenizer.graph.select(paths)
                selectedPath = paths[best]
            return self.tokenizer.graph.words(selectedPath)
        return []


class Tokenizer(object):
    """Vietnamese Tokenizer
    """

    def __init__(self, lexicon_src = None, regexp_src = None, bigramFilename = None,
                whilespaceModelFilename=None):
        """Construct the tokenizer

        Parameters
        -----------
        lexicon_src: str or list of str
            If string is provided, loader will treat it as xml file and parsing it to build the trie tree.
            Otherwise, the loader will treat it as lexicon string of list.

        regexp_src: str
            the filename of regular expression file. we use the regexp to classify the token category.
        """
        # load lexicon prefix tree(trie tree)
        import os
        this_dir, this_filename = os.path.split(__file__)

        # use default files if not provided
        if not lexicon_src:
            lexicon_src = os.path.join(this_dir, 'dat/tok/lexicon.xml')
        if not regexp_src:
            regexp_src = os.path.join(this_dir, 'dat/tok/regexp-py.txt')
        if not bigramFilename:
            bigramFilename = os.path.join(this_dir, 'dat/tok/syllables2M.arpa')
            
        self.lexicon = Lexicon()

        if type(lexicon_src) is str:
            self.lexicon.load(lexicon_src)
        else:
            self.lexicon.loadFromList(lexicon_src)

        self.classifier = None
        self.graph = PhraseGraph(self)
        self.graph2 = PhraseGraph2(self)

        logger.debug('Loading pattern file.')
        # regex
        self.patterns = {}
        regFile = open(regexp_src, 'r', encoding='utf8')
        lines = regFile.readlines()
        for curLine in lines:
            curLine = curLine.strip()

            # skip the remark line
            if curLine != '' and curLine[0] != '#':
                logger.debug('processing line: {}'.format(curLine))
                tokens = curLine.split('\t')
                logger.debug('len of tokens: {}'.format(len(tokens)))
                if len(tokens) == 2:
                    ptn_names = tokens[0].split(':')
                    if len(ptn_names) == 1:
                        logger.debug('Pattern {} added'.format(ptn_names[0]))
                        self.patterns[ptn_names[0]] = regex.compile(tokens[1])
                    else:
                        logger.debug('Pattern {} added'.format(ptn_names[1]))
                        self.patterns[ptn_names[1]] = regex.compile(tokens[1])
        regFile.close()

        if bigramFilename is not None:
            self.bigrams = Bigrams(bigramFilename)
        else:
            self.bigrams = None

    def tokenize(self, inputFilename, outputFilename):
        with open(inputFilename, 'r', encoding='utf8') as fin, open(outputFilename, 'w', encoding='utf8') as fout:
            lines = fin.readlines()
            for line in lines:
                tokenizeResult = self.tokenizeLine (line, concat=True)

                fout.write(' '.join(tokenizeResult))
                fout.write('\n')
                # write to output file

    def tokenizeLine(self, line: str, concat=False) -> list:
        seg = SegmentationFunction(self)

        line = line.strip()

        tokens = seg.segment(line)
        lstRet = list()

        for i in range(len(tokens)):
            curToken = tokens[i]
            if concat:
                if (curToken[0] == 'phrase' or curToken[0] == 'word'):
                    lstRet.append({
                        'Type': curToken[0],
                        'Text': curToken[1].replace(' ', '_')
                    })
                else:
                    lstRet.append({
                        'Type': curToken[0],
                        'Text': curToken[1],
                    })
            else:
                lstRet.append({
                    'Type': curToken[0],
                    'Text': curToken[1],
                })

        return lstRet
