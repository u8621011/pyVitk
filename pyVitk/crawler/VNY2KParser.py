""" Crawl and parse the VNY2K website into machine loadable format.(JOSN)

The information we try to parse out from site of Tu Nguyen Han Viet
[{
    "SearchWord": "中文",
    "VietnameseWord": "chữHán",
    "ChineseWord": "中文",
    "Pinyin": "Zhōngwén",
    "HanViet": "Trungvăn",
    "Synonyms": [
        "Trungvăn",
        "chữTàu",
        "tiếngTàu",
        "chữHán"
    ],
}]

"""

import requests
from bs4 import BeautifulSoup
import regex
import logging
from pyVitk.DictionaryLexicon import DictionaryLexicon


logger = logging.getLogger(__name__)

RE_SYNONYMS_ITEM = r"((?P<snum>\(\d+\)) (?P<stext>[\p{Ll}\p{Lu}]+),+\s+)"
RE_SYNONYMS_ITEM_PART = r"\(\d+\) [\p{Ll}\p{Lu}]+(, \(\d+\) [\p{Ll}\p{Lu}]+)*"
RE_ASIA_CHAR = r"(?P<asia>[\u4e00-\u9fff]+)"
RE_HANVIET_PART = r"(?P<chinese>[\u4e00-\u9fff]+)\s+(?P<pinyin>[\p{Ll}\p{Lu}]+)\s+\((?P<hanviet>[\p{Ll}\p{Lu}]+)\)"
RE_EXPLAIN_PART = r"\[.+\]"

re_synonyms_item = regex.compile(RE_SYNONYMS_ITEM)
re_synonyms_part = regex.compile(RE_SYNONYMS_ITEM_PART)
re_exp_part = regex.compile(RE_EXPLAIN_PART)
re_hanviet_part = regex.compile(RE_HANVIET_PART)

def parse_vny2k(w):
    url_hanviet = "http://vny2k.com/hannom/tunguyen.asp"
    r = requests.post(url_hanviet, data = {
        'u_search': w
    })

    r.encoding = "utf-8"

    result_bank = []    
    if r.status_code == 200:
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        for tbl in soup.find_all('table'):
            trs = tbl.find_all('tr')
            if len(trs[0].find_all('td')) == 2: # the found lexicon have 2 td tags
                result = DictionaryLexicon()
                result.source_language = 'zh-TW'
                result.target_language = 'vi-VN'
                result.source_title = w
                result.synonyms = []

                for r in tbl.find_all('tr')[1:]:
                    tds = r.find_all('td')

                    result.target_title = tds[0].string

                    detail_string = " ".join(tds[1].strings)
                    m = re_synonyms_part.match(detail_string)
                    if m:
                        logger.debug('full match of sym part: %r', m.group(0))
                        synonyms_string = m.group(0)
                        m_syn = re_synonyms_item.finditer(synonyms_string)
                        for cur_m in m_syn:
                            logger.debug('stext of sym part: %r', cur_m.group('stext'))
                            result.synonyms.append(cur_m.group('stext'))
                    else:
                        logger.debug('sym part not found')

                    m_hv = re_hanviet_part.search(detail_string)
                    if m_hv:
                        result.pron_systems.append({
                            'name': 'HanViet',
                            'pronunciation': m_hv.group('hanviet')
                        })
                        result.pron_systems.append({
                            'name': 'Pinyin',
                            'pronunciation': m_hv.group('pinyin'),
                        })
                        logger.debug('full match of hanviet part: %r', m_hv.group(0))
                        logger.debug('chinese of hanviet: %r', m_hv.group('chinese'))
                        logger.debug('pinyin of hanviet: %r', m_hv.group('pinyin'))
                        logger.debug('hanviet of hanviet: %r', m_hv.group('hanviet'))

                    m_exp = re_exp_part.search(detail_string)
                    if m_exp:
                        logger.debug('full match of exp part: %r', m_exp.group(0))

                    result_bank.append(result)
            else:
                logger.debug('Unknown lexicon: %r', w)
    else:
        logger.error('Cannot query from site:%r, status_code: %r', url_hanviet, r.status_code)
    return result_bank

