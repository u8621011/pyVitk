# coding=UTF-8

from .Tokenizer import Tokenizer
from .VNY2KParser import parse_vny2k
import logging

logger = logging.getLogger(__name__)
if not len(logger.handlers):
    # file handler
    hdlr = logging.FileHandler('pyVitk.log', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)

name = "pyVitk"

