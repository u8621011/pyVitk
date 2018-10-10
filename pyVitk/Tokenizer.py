# coding=UTF-8

import sys
import regex
import logging
from typing import List
from .Lexicon import Lexicon
from .Bigrams import Bigrams
from .Dijkstra import Dijkstra
from pyVitk.DataStructure import LexiconToken


logger = logging.getLogger(__name__)


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

    def words(self, path: list, concat=False) -> list:
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
                if concat:
                    lstSyllables.append('_')
                else:
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

    def segment(self, sentence: str, concat=False) -> list:
        """
        Segment the passed in sentence, caller must not call sentence.strip, segmentation function will do it to calculate the pricise term position in sentence.
        :param sentence:
        :return:
        """
        tokens = []

        s = sentence.lstrip()
        if len(s) == 0:
            return tokens

        # the first position of non-space char.
        cur_pos = len(sentence) - len(s)

        token_start_pos_base = cur_pos
        while True:
            max_matched_len = 0
            next_token = None
            token_type = None

            # greedy search for the longest pattern from the beginning of 's'
            logger.debug('Segmenting sentence: %s', s)
            for k, p in self.tokenizer.patterns.items():
                # return matchobject if matches
                m = p.match(s)
                if m:
                    logger.debug('【%s】 matched pattern: %s', s, k)
                    cur_matched_len = m.end(0) - m.start(0)
                    if max_matched_len < cur_matched_len:
                        max_matched_len = cur_matched_len
                        next_token = m.group(0)
                        token_type = k

                        # what pattern will have space in the begin or end of matched term?
                        stripped_token = next_token.strip()
                        if len(stripped_token) != len(next_token):
                            logger.info('Found the case of token need to be stripped, token: [%s]', next_token)
                            raise Exception('Found the case of token need to be stripped')

            if token_type:
                logger.debug('longest matched pattern type: %s, token: %s', token_type, next_token)
            else:
                logger.debug('Cannot find the matched pattern. sentence: %s', s)

            # split off the longest token we found.
            if next_token:
                string_left = s[max_matched_len:]
                string_left_trimmed = s[max_matched_len:].lstrip()

                # process the token we found
                if 'name' in token_type and len(string_left_trimmed) > 0:   # we have dropped the name regex pattern.
                    tup = self.processName(next_token, string_left_trimmed)
                    if len(tup[0]) != len(next_token):
                        next_token = tup[0]
                        s = string_left_trimmed = tup[1]
                        token_type = 'word'

                    logger.debug('appending new token, type: {}, token: {}'.format(token_type, next_token))
                    tokens.append((token_type, next_token))
                elif 'unit' in token_type and len(string_left_trimmed) > 0:
                    tup = self.processUnit(next_token, string_left_trimmed)
                    if len(tup[0]) > len(next_token):
                        next_token = tup[0]
                        s = string_left_trimmed = tup[1]
                        token_type = "unit"
                    else:
                        s = string_left_trimmed

                    token_start_pos = token_start_pos_base
                    token_end_pos = token_start_pos + len(next_token)
                    token_start_pos_base = token_end_pos + (
                            len(string_left) - len(string_left_trimmed))  # the next base
                    logger.debug('appending new token, type: %s, token: %s', token_type, next_token)
                    t = LexiconToken(type=token_type, text=next_token,
                                     start_char_pos=token_start_pos, end_char_pos=token_end_pos)
                    tokens.append(t)
                elif 'phrase' in token_type:
                    if next_token.find(' ') > 0:    # multi-syllabic phrase
                        if self.tokenizer.classifier is not None:
                            raise NotImplementedError
                        else:
                            # segment the phrase using a phrase graph
                            words = self.tokenizePhrase(next_token, concat)
                            if words is not None:
                                token_start_pos = token_start_pos_base
                                for i in range(len(words)):
                                    if i != 0:
                                        token_start_pos = token_end_pos + 1   # every token must be split by one space
                                    token_end_pos = token_start_pos + len(words[i])
                                    t = LexiconToken(type="word", text=words[i], start_char_pos=token_start_pos
                                                     , end_char_pos=token_end_pos)
                                    tokens.append(t)
                            else:
                                raise Exception('Error when tokenizing phrase: ' + next_token)
                    else:
                        token_start_pos = token_start_pos_base
                        token_end_pos = token_start_pos_base + max_matched_len
                        t = LexiconToken(type="word", text=next_token, start_char_pos=token_start_pos,
                                         end_char_pos=token_end_pos)
                        tokens.append(t)
                    s = string_left_trimmed
                    token_start_pos_base = token_end_pos + (
                            len(string_left) - len(string_left_trimmed))  # the next base
                else:
                    token_start_pos = token_start_pos_base
                    token_end_pos = token_start_pos_base + max_matched_len
                    t = LexiconToken(type=token_type, text=next_token, start_char_pos=token_start_pos,
                                     end_char_pos=token_end_pos)
                    tokens.append(t)
                    s = string_left_trimmed
                    token_start_pos_base = token_end_pos + (
                                len(string_left) - len(string_left_trimmed))  # the next base
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


    def tokenizePhrase(self, phrase: str, concat=False)->List[str]:
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
            return self.tokenizer.graph.words(selectedPath, concat)
        return []


class Tokenizer(object):
    """Vietnamese Tokenizer
    """

    def __init__(self, lexicon_src=None, regexp_src=None, bigramFilename=None,
                whilespaceModelFilename=None, case_sensitive=False):
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
        if not regexp_src:
            regexp_src = os.path.join(this_dir, 'dat/tok/regexp-py.txt')
        if not bigramFilename:
            bigramFilename = os.path.join(this_dir, 'dat/tok/syllables2M.arpa')

        if lexicon_src:
            self.lexicon = Lexicon(default=False, case_sensitive=case_sensitive)
            if type(lexicon_src) is str:
                self.lexicon.load(lexicon_src)
            else:
                self.lexicon.loadFromList(lexicon_src)
        else:
            self.lexicon = Lexicon(case_sensitive=case_sensitive)

        self.classifier = None
        self.graph = PhraseGraph(self)

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

    def get_lexicons_list(self) -> List[str]:
        """"Return list of lexicon strings. None if lexicon of tokenzier is not initialized properly.
        """
        if self.lexicon:
            return self.lexicon.flatten_to_list()

        return None

    def to_lexicon_xml_file(self, ofile: str):
        """Serialize the lexicon sturcture into xml file
        """
        self.lexicon.serialize_to_xml(ofile)

    def insertLexicons(self, lexicons: list):
        """runtime insert lexicon

            :param lexicons: the list of inserting lexicon string
            :returns: the list of lexicons inserted
            """
        inserted = []
        for l in lexicons:
            if not self.lexicon.hasWord(l):
                inserted.append(l)
                self.lexicon.insertWord(l)
        logger.debug('The additional lexicons inserted: {}'.format(len(inserted)))

        return inserted
            
    def tokenize(self, inputFilename, outputFilename):
        with open(inputFilename, 'r', encoding='utf8') as fin, open(outputFilename, 'w', encoding='utf8') as fout:
            lines = fin.readlines()
            for line in lines:
                tokenizeResult = self.tokenizeLine (line, concat=True)

                fout.write(' '.join(tokenizeResult))
                fout.write('\n')
                # write to output file

    def tokenizeLine(self, line: str, concat=False) -> list:
        """
        Line Tokenizing.  Precondition of calling this:
        1. line must be newline char dropped before calling
        :param line:
        :param concat:
        :return:
        """
        seg = SegmentationFunction(self)

        tokens = seg.segment(line, concat)

        return tokens
