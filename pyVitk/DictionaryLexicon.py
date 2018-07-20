# encoding=utf-8

"""The data struction for Dictionary Lookup Result

{
    "source_language": "zh-TW",
    "target_language": "vi-VN",
    "source_title": "中文",
    "target_title": "chữHán",
    pron_system: [
        {
            "name": "Pinyin",
            "pronunciation":"Zhōngwén",
        },
        {
            "name": "HanViet",
            "pronunciation":"Trungvăn",
        }
    ],
    "synonyms": [
        "Trungvăn",
        "chữTàu",
        "tiếngTàu",
        "chữHán"
    ],
}
"""

import json

class DictionaryLexicon(object):
    def __init__(self):
        self.source_language = None
        self.target_language = None
        self.source_title = None
        self.target_title = None
        self.pron_systems = []
        self.synonyms = []

