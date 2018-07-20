# encoding = utf-8

"""Crawler & parser of vdict website

website sample:
https://vdict.com/%E8%A6%81,8,0,0.html
https://vdict.com/%E5%A7%93%E5%90%8D,8,0,0.html
https://vdict.com/%E4%B8%AD%E6%96%87,8,0,0.html
https://vdict.com/%E6%8F%9B,8,0,0.html
https://vdict.com/%E6%89%BE%E4%B8%8D%E5%88%B0%E6%88%91,8,0,0.html
https://vdict.com/%E5%96%9D,8,0,0.html
"""

import requests
from bs4 import BeautifulSoup
from pyVitk.DictionaryLexicon import DictionaryLexicon
import json
import regex
import logging

RE_MULTI_MEANINGS = r"\d+\.(?P<words>[\w ,]+)\n*"

re_multi_meaings = regex.compile(RE_MULTI_MEANINGS)
logger = logging.getLogger(__name__)


def parse_vdict(src_lang, tar_lang, w):
    """  src_lang, tar_lang not supported yet.
    """
    url_ptn = "https://vdict.com/{},8,0,0.html"
    url_string = url_ptn.format(w)
    r = requests.get(url_string)

    r.encoding = "utf-8"

    result_bank = []
    if r.status_code == 200:
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        content_div = soup.find(id="contents")
        content_tbls = content_div.find_all('table')
        for tbl in content_tbls:
            lex = DictionaryLexicon()
            lex.source_language = 'zh-TW'
            lex.target_language = 'vi-VN'
            lex.source_title = w

            hv = tbl.find_all('div', class_='hv_NameTitle')
            if hv and len(hv) > 0:
                lex.pron_systems.append({
                    'HanViet': hv[0].a.string
                })

            meaning = tbl.find_all('blockquote')
            if meaning and len(meaning) > 0:
                matches = re_multi_meaings.findall(meaning[0].span.text)
                if len(matches) > 0:
                    meanings = matches
                else:
                    meanings = meaning[0].span.text.split(',')
                meanings = [m.strip() for m in meanings]
                lex.target_title = meanings[0]
                if len(meanings) > 1:
                    lex.synonyms.extend(meanings[1:])

            result_bank.append(lex)
    return result_bank

