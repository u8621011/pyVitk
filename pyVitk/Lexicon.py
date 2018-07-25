# coding=UTF-8

import xml.etree.ElementTree as etree
import sys
from nltk.collections import Trie
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Node(object):
    def __init__(self, c):
        self.c = c
        self.children = []

    def addChild(self, newNode):
        # add the child to the correct position
        index = 0
        childLen = len(self.children)
        while (index < childLen) and (self.children[index].c < newNode.c):
            index += 1
        self.children.insert(index, newNode)

    def insertWord(self, s: str, pos: int):
        """ build the trie nodes from string
        """
        if pos == len(s):
            # end char already exist?
            for j in range(0, len(self.children)):
                if self.children[j].c == '*':
                    return

            node = Node('*')
            self.children.append(node)
            return

        # already have node of current char?
        cur_node = None
        for j in range(0, len(self.children)):
            n = self.children[j]
            if n.c == s[pos]:
                cur_node = n
                break

        # not exist, create new node for current char
        if not cur_node:
            cur_node = Node(s[pos])
            self.children.append(cur_node)

        cur_node.insertWord(s, pos + 1)

    def hasWord(self, s: str, pos: int) -> bool:
        if pos == len(s):
            for j in range(0 , len(self.children)):
                if self.children[j].c == '*':
                    return True
            return False
        for j in range(0, len(self.children)):
            n = self.children[j]
            if n.c == s[pos]:
                return n.hasWord(s, pos + 1)
        return False


class Lexicon(object):
    """Load and build prefix tree from lexcion.xml"""
    def __init__(self):
        # the original trie implementation
        # self.root = Node('_')
        self.root = None
        self.numNodes = 0

        #self.trie = Trie()
        self.trie = None
    def load(self, filename: str):
        xml = etree.parse(filename)
        n = xml.getroot()
        self.root = self.loadNode(n)

    def loadFromList(self, lex_list):
        """Load lexicon from string list

        Parameters
        ----------
        lex_list: list of str

        """
        self.trie = Trie()

        for item in lex_list:
            self.trie.insert(item)

    def loadNode (self, n):
        node = Node(n.attrib['c'])
        for child in n:
            c = self.loadNode(child)
            node.addChild(c)
        self.numNodes += len(n.getchildren())

        return node

    def insertWord(self, word: str):
        if self.root:
            self.root.insertWord(word, 0)
        elif self.trie:
            self.trie.insert(word)
        else:
            raise ValueError('Dunno the type of trie tree structure.')

    def hasWord(self, word: str) -> bool:
        if self.root:
            return self.hasWordOrg(word)
        elif self.trie:
            return self.hasWordTrie(word)
        else:
            raise ValueError('Lexicon Dictionary is not be initialized')

    def hasWordOrg(self, word: str) -> bool:
        return self.root.hasWord(word, 0)

    def hasWordTrie(self, text):
        if self.trie:
            n = len(text)
            curTrie = self.trie
            for i in range(n):
                if text[i] in curTrie:
                    curTrie = curTrie[text[i]]
                else:
                    return False
            if Trie.LEAF in curTrie:
                return True

        else:
            return False

    def serialize_to_xml(self, ofile: str):
        if self.root:
            # build ElementTree from root structure
            et_root = etree.Element('n', attrib={'c': '_'})
            if len(self.root.children) > 0:
                for child in self.root.children:
                    if child.c == '*':
                        etree.SubElement(et_root, 'n', {'c': '*'})
                    else:
                        et_child = etree.SubElement(et_root, 'n', {'c': child.c})
                        self.build_etree_from_node(et_child, child)
            else:
                etree.SubElement(et_root, 'n', {'c': '*'})

            tree = etree.ElementTree(et_root)
            tree.write(ofile, encoding='utf-8', xml_declaration=True)
        else:
            raise NotImplementedError

    def build_etree_from_node(self, et_parent, node_parent):
        if node_parent.children is not None and len(node_parent.children) > 0:
            for child in node_parent.children:
                if child.c == '*':
                    etree.SubElement(et_parent, 'n', {'c': '*'})
                else:
                    et_child = etree.SubElement(et_parent, 'n', {'c': child.c})
                    self.build_etree_from_node(et_child, child)
        else:
            etree.SubElement(et_parent, 'n', {'c': '*'})


    def flattenToFile(self, outFilename: str):
        f = open(outFilename, 'w',  encoding='utf8')
        curCharList = []
        for child in self.root.children:
            if child.c == '*':
                f.write(''.join(curCharList))
                f.write('\n')
            else:
                curCharList.append(child.c)
                self.flttenRecursive(f, child, curCharList)
                curCharList.pop()

        f.close()

    def flttenRecursive(self, fwrite, nodeHead: Node, charList: list):
        for child in nodeHead.children:
            if child.c == '*':
                fwrite.write(''.join(charList))
                fwrite.write('\n')
            else:
                charList.append(child.c)
                self.flttenRecursive(fwrite, child, charList)
                charList.pop()

if __name__ == '__main__':
    cmd = sys.argv[1]

    if cmd == 'load':
        n = datetime.now()
        l = Lexicon()
        l.load(sys.argv[2])
        d = datetime.now() - n
        logger.debug('timedelta to run: {}'.format(d))
    elif cmd == 'flat':
        l = Lexicon()
        l.flattenToFile(sys.argv[2])
    elif cmd == 'loadflat':
        n = datetime.now()
        with open(sys.argv[2], encoding='utf8') as f:
            l = Lexicon()
            for line in f:
                if len(line) > 0:
                    l.trie.insert(line)

        d = datetime.now() - n
        logger.debug('timedelta to run: {}'.format(d))

