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
from pyVitk import parse_vny2k

r = parse_vny2k('中文')

print(r)
```