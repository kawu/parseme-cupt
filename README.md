# Python CUPT parser

This repository provides a Python parser for the [CUPT format][cupt].  It's in
an early stage of development, expect substantial changes!

# Installation

Using `pip`:

    git clone https://github.com/kawu/parseme-cupt.git
    cd parseme-cupt
    pip install .

# Example

### Retrieval

To parse text in the CUPT format, use the [CoNLL-U Python parser][conllu]
(which is a dependency of the CUPT parser).  For instance:
```python
>>> import conllu
>>>
>>> data = """
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE
# source_sent_id = . . 4045
# text = Worse yet, what is going on will not let us alone.
1       Worse   bad     ADJ     CMP     _       10      advmod  _       _       *
2       yet     yet     ADV     _       _       1       advmod  _       SpaceAfter=No   *
3       ,       ,       PUNCT   Comma   _       1       punct   _       _       *
4       what    what    PRON    WH      _       6       nsubj   _       _       *
5       is      be      AUX     PRES-AUX        _       6       aux     _       _       *
6       going   go      VERB    ING     _       10      csubj   _       _       2:VPC.full
7       on      on      ADV     _       _       6       compound:prt    _       _       2
8       will    will    AUX     PRES-AUX        _       10      aux     _       _       *
9       not     not     PART    NEG     _       10      advmod  _       _       *
10      let     let     VERB    INF     _       0       root    _       _       1:VID
11      us      we      PRON    PERS-P1PL-ACC   _       10      obj     _       _       *
12      alone   alone   ADJ     POS     _       10      xcomp   _       SpaceAfter=No   1
13      .       .       PUNCT   Period  _       10      punct   _       _       *

"""
>>> sentences = conllu.parse(data)
>>> sentence = sentences[0]   # the dataset contains one sentence
```
You can then retrieve the MWE instances occurring in the individual sentences
using `retrieve_mwes`:
```python
>>> import parseme.cupt as cupt
>>>
>>> print(cupt.retrieve_mwes(sentence))
TODO
```

### Update

To clear MWE annotations in a given sentence, use `clear_mwes`:
```python
>>> cupt.clear_mwes(sentence)
>>> print(sentence.serialize())
TODO
```
One way to add new MWE annotations is using `add_mwe`:
```python
>>> from parseme.cupt import MWE
>>>
>>> cupt.add_mwe(sentence, mwe_id=1, mwe=MWE('VPC.full', frozenset([6, 7])))
>>> print(cupt.retrieve_mwes(sentence))
TODO
```
A safer alternative, which in particular deals with the MWE identifiers
automatically, is to add all target MWE annotations at once using
`replace_mwes`:
```python
>>> mwe1 = MWE('VPC.full', frozenset([6, 7]))
>>> mwe2 = MWE('VID', frozenset([10, 12]))
>>> cupt.replace_mwes(sent, set([mwe1, mwe2]))
>>> print(cupt.retrieve_mwes(sentence))
TODO
```






[cupt]: http://multiword.sourceforge.net/cupt-format "CUPT format"
[conllu]: https://pypi.org/project/conllu/ "Python CoNLL-U parser"
