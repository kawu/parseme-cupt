# Python CUPT parser

This repository provides a Python parser for the [CUPT format][cupt].  It's in
an early stage of development, expect substantial changes!

# Installation

Using `pip`:

    git clone https://github.com/kawu/parseme-cupt.git
    cd parseme-cupt
    pip install .

# Example

To read and parse a `test.cupt` file, use the [CoNLL-U Python parser][conllu]
(which is a dependency of the CUPT parser).  For instance:
```python
from conllu import parse
with open ("test.cupt", "r") as f:
    data = f.readlines()
    sentences = parse(''.join(data))
```
You can then retrieve the MWE instances occurring in the individual sentences
using `retrieve_mwes`, for instance:
```python
from parseme.cupt import retrieve_mwes
for sent in sentences:
   mwes = retrieve_mwes(sent)
   print(mwes)
```


[cupt]: http://multiword.sourceforge.net/cupt-format "CUPT format"
[conllu]: https://pypi.org/project/conllu/ "Python CoNLL-U parser"
