from pyairtable.formulas import *


def INCLUDE(what: str, where: FIELD, start_position=0) -> str:
    """
    Creates an FIND statement

    >>> FIND(STR(2021), FIELD('DatetimeCol'))
    'FIND('2021', {DatetimeCol})'

    Args:
        what: String to search for
        where: Where to search. Must be a field reference.
        start_position: Index of where to start search. Default is 0.

    """
    if start_position:
        return "FIND({}, ARRAYJOIN({}), {})".format(what, where, start_position)
    else:
        return "FIND({}, ARRAYJOIN({}))".format(what, where)


def OR(*args) -> str:
    """
    Creates an OR Statement

    >>> OR(1, 2, 3)
    'OR(1, 2, 3)'
    """
    return "OR({})".format(",".join(args))
