# pyVitk
Python Version Vietnamese Text Processing Toolkit.


# API
- tokenizeLine: tokenize the line of vietnamese sentence into tokens  
This vietnamese tokenzier is  porting from vn.vitk of Lê Hồng Phương.  
The original vn.vitk project is [here](https://github.com/phuonglh/vn.vitk).

Usage
```python
from pyVitk import Tokenizer

t = Tokenizer()
sentence = "bài viết chọn lọc alt hình ảnh chọn lọc"
tokens = t.tokenizeLine(sentence, concat=True)

print("tokenize result: {}".format(str(tokens)))
```

- parse_vny2k: to crawl and parse dictionary of han-viet.net

Usage
```python
from pyVitk import crawler
import json

# support zh-TW to vi-VN currently. will return DictionaryLexicon structure
results = crawler.parse_vdict('zh-TW', 'vi-VN', '中文')
results_y2k = crawler.parse_vny2k('中文')

print(json.dumps(results.__dict__))
print(json.dumps(results_y2k.__dict__))

```