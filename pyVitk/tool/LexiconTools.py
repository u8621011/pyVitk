import sys
import logging
from datetime import datetime
from ..Lexicon import Lexicon
from ..helper import setup_logging


setup_logging()
logger = logging.getLogger(__name__)

cmd = sys.argv[1]
if cmd == 'flat':
    l = Lexicon()
    l.flattenToFile(sys.argv[2])
elif cmd == 'loadflat':
    n = datetime.now()
    with open(sys.argv[2], encoding='utf8') as f:
        l = Lexicon()
        for line in f:
            if len(line) > 0:
                l.insertWord(line)

    d = datetime.now() - n
    logger.debug('timedelta to run: {}'.format(d))
elif cmd == "create_insensitive_xml":   # create lexicon-insensitive.xml
    import os

    this_dir, this_filename = os.path.split(__file__)
    lexicon_src = os.path.join(this_dir, 'lexicon.txt')
    lexicon_xml = os.path.join(this_dir, 'lexicon-insensitive.xml')

    l = Lexicon(default=False, case_sensitive=False)
    f_lex = open(lexicon_src, mode='r', encoding='utf-8')

    logger.info('Building trie tree from lexicon.txt')
    lexes = [lex.strip() for lex in f_lex.readlines()]
    for lex in lexes:
        if len(lex) > 0:
            l.insertWord(lex)

    logger.info('Write to lexicon-insensitive.xml file')
    l.serialize_to_xml(lexicon_xml)