#   encoding: utf-8

""""Parser for http://hvdic.thivien.net
Will try to parse out the han viet relationship
"""

import requests
from bs4 import BeautifulSoup
from pyVitk.DictionaryLexicon import DictionaryLexicon
from opencc import OpenCC

cc = OpenCC('s2t')

def parse_hanviet_from_vn(w):
    url_ptn = "http://hvdic.thivien.net/hv/{}"
    url_string = url_ptn.format(w)
    r = requests.get(url_string)

    r.encoding = "utf-8"

    result_bank = {}
    if r.status_code == 200:
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        for info_div in soup.find_all('div', class_='info'):
            hanviet_spans = info_div.find_all('span')
            for s in hanviet_spans:
                # the hanviet span format of vietnamese lookup is 【中文 trung văn】
                span_tokens = s.string.split()
                cht_text = cc.convert(span_tokens[0])
                hanviet_text = ' '.join(span_tokens[1:])

                if cht_text in result_bank:
                    lex = result_bank[cht_text]
                else:
                    lex = DictionaryLexicon()
                    lex.source_language = 'zh-TW'
                    lex.target_language = 'vi-VN'
                    lex.source_title = cht_text
                    result_bank[cht_text] = lex

                lex.pron_systems.append({
                    'name': 'HanViet',
                    'pronunciation': hanviet_text,
                })

    return result_bank.values()


def parse_hanviet(w):
    url_ptn = "http://hvdic.thivien.net/whv/{}"
    url_string = url_ptn.format(w)
    r = requests.get(url_string)

    r.encoding = "utf-8"

    result_bank = []
    if r.status_code == 200:
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        lex = DictionaryLexicon()
        lex.source_language = 'zh-TW'
        lex.target_language = 'vi-VN'
        lex.source_title = w
        for info_div in soup.find_all('div', class_='info'):
            hanviet_spans = info_div.find_all('span')
            for s in hanviet_spans:
                lex.pron_systems.append({
                    'name': 'HanViet',
                    'pronunciation': s.string,
                })

        result_bank.append(lex)

    return result_bank
