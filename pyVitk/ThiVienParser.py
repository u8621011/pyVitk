#   encoding: utf-8

""""Parser for http://hvdic.thivien.net
Will try to parse out the han viet relationship
Return samples:

[
    {
        "ChineseWord": "文",
        "HanViet": "văn",
    }, {
        "ChineseWord": "文",
        "HanViet": "vấn",
    }
]
"""

import requests
from bs4 import BeautifulSoup


def parse_hanviet(w):
    url_ptn = "http://hvdic.thivien.net/whv/{}"
    url_string = url_ptn.format(w)
    r = requests.get(url_string)

    r.encoding = "utf-8"

    result_bank = []
    if r.status_code == 200:
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        for info_div in soup.find_all('div', class_='info'):
            hanviet_spans = info_div.find_all('span')
            for s in hanviet_spans:
                result_bank.append({
                    'ChineseWord': w,
                    'HanViet': s.string,
                })

    return result_bank

