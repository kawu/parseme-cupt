from typing import Union, NamedTuple, FrozenSet, Dict, Optional, Set
from collections import OrderedDict

from conllu import TokenList


# Constants
MWE_FIELD = "parseme:mwe"
MWE_NONE = "*"
MWE_UNKOWN = "_"


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


def _join_mwes(x: MWE, y: MWE) -> MWE:
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


def _update_dict_with(d: Dict[MweID, MWE], new: Dict[MweID, MWE]):
    """Update the first dictionary with MWEs from the second dictionary."""
    for ix in new.keys():
        if ix in d:
            mwe = _join_mwes(d[ix], new[ix])
        else:
            mwe = new[ix]
        d[ix] = mwe


def _mwes_in_tok(tok: OrderedDict) -> Dict[MweID, MWE]:
    """Extract MWE fragments annotated for the given token."""
    mwe_anno = tok["parseme:mwe"]
    if mwe_anno in [MWE_NONE, MWE_UNKOWN]:
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
        tok_mwes = _mwes_in_tok(tok)
        _update_dict_with(result, tok_mwes)
    return result


def clear_mwes(sent: TokenList, value=MWE_NONE):
    """Clear all MWEs annotations in the given sentence."""
    for tok in sent:
        tok[MWE_FIELD] = value


def unsafe_add_mwe(sent: TokenList, mwe_id: MweID, mwe: MWE):
    """Add the MWE with the given ID to the given sentence.

    The function does not check if a MWE with the given ID already
    exists, neither if a MWE with the same category and the same
    set of tokens already exists in the sentence.  Use with caution.
    """
    # Retrieve the list of tokens as a sorted list
    tok_ids = sorted(mwe.toks)

    # Check some invariants, just in case
    assert len(tok_ids) >= 1
    assert tok_ids[0] == min(tok_ids)

    # Create a dictionary from token IDs to actual tokens
    tok_map = {}
    for tok in sent:
        tok_map[tok['id']] = tok

    # Helper function
    def update(tok_id, mwe_str):
        tok = tok_map[tok_id]
        if tok[MWE_FIELD] in [MWE_NONE, MWE_UNKOWN]:
            tok[MWE_FIELD] = mwe_str
        else:
            tok[MWE_FIELD] += ";" + mwe_str

    # Update the first MWE component token
    mwe_str = ":".join([str(mwe_id), mwe.cat])
    update(tok_ids[0], mwe_str)

    # Update the remaining MWE component tokens
    mwe_str = str(mwe_id)
    for tok_id in tok_ids[1:]:
        update(tok_id, mwe_str)


def replace_mwes(sent: TokenList, mwes: Set[MWE]):
    """Replace the MWE annotations in the sentence with new MWEs."""
    clear_mwes(sent)
    mwe_id = 1
    for mwe in mwes:
        unsafe_add_mwe(sent, mwe_id, mwe)
        mwe_id += 1
