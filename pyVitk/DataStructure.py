# encoding=utf-8
import json


class LexiconToken(object):
    def __init__(self, type, text, start_char_pos, end_char_pos):
        self.type = type
        self.text = text
        self.start_char_pos = start_char_pos
        self.end_char_pos = end_char_pos

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__,  ensure_ascii=False, indent=4)