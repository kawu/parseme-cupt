from typing import Union, NamedTuple, FrozenSet, Dict, Optional
from collections import OrderedDict

# import conllu
from conllu import TokenList


# Token ID is normally a single number (1, 2, ...), but it can be also
# a three-element tuple in special situations, for instance:
# * "1.1" => (1, '.', 1)
# * "1-2" => (1, '-', 2)
TokID = Union[int, tuple]

# MWE identifier (has the scope of the corresponding sentence)
MweID = int

# MWE category
MweCat = str


class MWE(NamedTuple):
    """MWE annotation"""
    cat: Optional[MweCat]
    toks: FrozenSet[TokID]


def join_mwes(x: MWE, y: MWE) -> MWE:
    """Join two MWEs into one.

    This requires that both input MWEs have the same category.
    Otherwise, an exception is raised (which would indicate that
    there's an annotation error in a .cupt file).
    """
    if x.cat and y.cat and x.cat != y.cat:
        raise Exception("cannot join MWEs with different categories")
    else:
        cat = x.cat or y.cat
        return MWE(cat, x.toks.union(y.toks))


def update_dict_with(d: Dict[MweID, MWE], new: Dict[MweID, MWE]):
    """Update the first dictionary with MWEs from the second dictionary."""
    for ix in new.keys():
        if ix in d:
            mwe = join_mwes(d[ix], new[ix])
        else:
            mwe = new[ix]
        d[ix] = mwe


def mwes_in_tok(tok: OrderedDict) -> Dict[MweID, MWE]:
    """Extract MWE fragments annotated for the given token."""
    mwe_anno = tok["parseme:mwe"]
    if mwe_anno == '*' or mwe_anno == '_':
        return dict()
    else:
        result = dict()
        tok_ids = frozenset([tok["id"]])
        for mwe_raw in mwe_anno.split(';'):
            mwe_info = mwe_raw.split(':')
            if len(mwe_info) == 2:
                (ix, cat) = mwe_info
            else:
                (ix,), cat = mwe_info, None
            result[int(ix)] = MWE(cat, tok_ids)
        return result


def retrieve_mwes(sent: TokenList) -> Dict[MweID, MWE]:
    """Retrieve MWEs from the given sentence."""
    result = dict()     # type: Dict[MweID, MWE]
    for tok in sent:
        tok_mwes = mwes_in_tok(tok)
        update_dict_with(result, tok_mwes)
    return result
