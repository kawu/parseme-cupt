# Python CUPT parser

This repository provides a Python parser for the [CUPT format][cupt].  It's in
an early stage of development, expect substantial changes!

# Installation

Using `pip`:

    git clone https://github.com/kawu/parseme-cupt.git
    cd parseme-cupt
    pip install .

# Example

To parse text in the CUPT format, use the [CoNLL-U Python parser][conllu]
(which is a dependency of the CUPT parser).  For instance:
```python
>>> from conllu import parse
>>>
>>> data = """
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE
# source_sent_id = . . 1644
# text = I give the floor to Mrs Green.
1       I       I       PRON    PERS-P1SG-NOM   _       2       nsubj   _       _       *
2       give    give    VERB    PRES    _       0       root    _       _       1:VID
3       the     the     DET     DEF     _       4       det     _       _       1
4       floor   floor   NOUN    SG-NOM  _       2       obj     _       _       1
5       to      to      ADP     _       _       7       case    _       _       *
6       Mrs     Mrs     NOUN    SG-NOM  _       7       compound        _       _       *
7       Green   green   PROPN   SG-NOM  _       2       obl     _       SpaceAfter=No   *
8       .       .       PUNCT   Period  _       2       punct   _       _       *

"""
>>> sentences = parse(data)
```
You can then retrieve the MWE instances occurring in the individual sentences
using `retrieve_mwes`, for instance:
```python
>>> from parseme.cupt import retrieve_mwes
>>>
>>> print(retrieve_mwes(sentences[0]))
{1: MWE(cat='VID', toks=frozenset({2, 3, 4}))}
```


[cupt]: http://multiword.sourceforge.net/cupt-format "CUPT format"
[conllu]: https://pypi.org/project/conllu/ "Python CoNLL-U parser"
