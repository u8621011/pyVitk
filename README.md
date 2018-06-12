# pyVitk
Python Version Vietnamese Text Processing Toolkit.

This is a vietnamese text tokenizer porting from vn.vitk of Lê Hồng Phương.

The original vn.vitk project is [here](https://github.com/phuonglh/vn.vitk).

# Usage
Simplest usage as below.

```python
from pyVitk import Tokenizer

t = Tokenizer()
sentence = "bài viết chọn lọc alt hình ảnh chọn lọc"
tokens = t.tokenizeLine(sentence, concat=True)

print("tokenize result: {}".format(str(tokens)))
```
