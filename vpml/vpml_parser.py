from abc import ABC, abstractmethod

import ply.yacc as yacc

from vpml.vpml_lexer import VpmlLexer

tokens = VpmlLexer.tokens


class ParseNode(ABC):
    @abstractmethod
    def to_dict(self):
        raise Exception("Not implement in derived class!")


class RootNode(ParseNode):
    def __init__(self, parse_tree: list[ParseNode], has_start: bool = False, has_end: bool = False):
        self.parse_tree = parse_tree
        self.has_start = has_start
        self.has_end = has_end

    def __repr__(self):
        return f'RootNode(has_start={self.has_start}, has_end={self.has_end}, parse_tree={repr(self.parse_tree)})'

    def to_dict(self):
        return {
            "root": {
                "has_start": self.has_start,
                "has_end": self.has_end,
                "parse_tree": [pt.to_dict() for pt in self.parse_tree]
            }
        }


class ExtractNode(ParseNode):
    def __init__(self, parse_tree: list[ParseNode]):
        self.parse_tree = parse_tree

    def __repr__(self):
        return f'ExtractNode(parse_tree={repr(self.parse_tree)})'

    def to_dict(self):
        return {
            "extract": {
                "parse_tree": [pt.to_dict() for pt in self.parse_tree]
            }
        }


class OrNode(ParseNode):
    def __init__(self, parse_tree: list[ParseNode]):
        self.parse_tree = parse_tree

    def __repr__(self):
        return f'OrNode(parse_tree={repr(self.parse_tree)})'

    def to_dict(self):
        return {
            "or": {
                "parse_tree": [pt.to_dict() for pt in self.parse_tree]
            }
        }


class SkipNode(ParseNode):
    def __init__(self, skip: int):
        self.skip = skip

    def __repr__(self):
        return f'SkipNode(skip={self.skip})'

    def to_dict(self):
        return {"skip": self.skip}


class WithinNode(ParseNode):
    def __init__(self, end: int, parse_tree: ParseNode):
        if end < 1:
            raise SyntaxError(f"Invalid value for 'within': {end}, MUST be '> 0'")
        self.end = end
        self.parse_tree = parse_tree

    def __repr__(self):
        return f'WithinNode(end={self.end}, parse_tree={repr(self.parse_tree)})'

    def to_dict(self):
        return {
            "within": {
                "end": self.end,
                "parse_tree": self.parse_tree.to_dict()
            }
        }


class BetweenNode(ParseNode):
    def __init__(self, lower: int, upper: int, parse_tree: list[ParseNode]):
        if lower < 1:
            raise SyntaxError(f"Invalid value for 'between' lower bound: {lower}, MUST be '> 0'")
        elif upper < 1:
            raise SyntaxError(f"Invalid value for 'between' upper bound: {upper}, MUST be '> 0'")
        elif upper < lower:
            raise SyntaxError(f"Invalid values for 'between' range: {upper}, MUST be '>' {lower}")
        self.lower = lower
        self.upper = upper
        self.parse_tree = parse_tree

    def __repr__(self):
        return f'BetweenNode(lower={self.lower}, upper={self.upper}, parse_tree={repr(self.parse_tree)})'

    def to_dict(self):
        return {
            "between": {
                "lower": self.lower,
                "upper": self.upper,
                "parse_tree": [pt.to_dict() for pt in self.parse_tree]
            }
        }


class PropertyNode(ParseNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'PropertyNode(prop={self.name})'

    def to_dict(self):
        return {"property": self.name}


class OpNode(ParseNode):
    def __init__(self, op: str, has_not: bool = False, no_case: bool = False):
        self.op = op
        self.has_not = has_not
        self.no_case = no_case

    def __repr__(self):
        return f'OpNode(op={self.op}, has_not={self.has_not}, no_case={self.no_case})'

    def to_dict(self):
        return {
            "op": {
                "op": self.op,
                "has_not": self.has_not,
                "no_case": self.no_case
            }
        }


class MatchNode(ParseNode):
    def __init__(self, prop: PropertyNode, op: OpNode, value: list | str):
        self.prop = prop
        self.op = op
        self.value = value

    def __repr__(self):
        value = ','.join(self.value) if isinstance(self.value, list) else self.value
        return f'MatchNode(kind={repr(self.prop)}, op={repr(self.op)}, value={value})'

    def to_dict(self):
        return {
            "match": {
                **self.prop.to_dict(),
                **self.op.to_dict(),
                "value": self.value
            }
        }


# ============================
# root -> START m_sq END
#      -> START m_sq
#      ->       m_sq END
#      ->       m_sq
# ----------------------------
def p_root_start_end(p):
    """root : START m_sq END"""
    p[0] = RootNode(has_start=True, has_end=True, parse_tree=p[2])


def p_root_start(p):
    """root : START m_sq"""
    p[0] = RootNode(has_start=True, parse_tree=p[2])


def p_root_end(p):
    """root : m_sq END"""
    p[0] = RootNode(has_end=True, parse_tree=p[1])


def p_root_no_start_end(p):
    """root : m_sq"""
    p[0] = RootNode(parse_tree=p[1])


# ============================
# m_sq -> m_opt_scope
#      -> skip
#      -> m_opt_scope m_sq
#      -> skip        m_sq
#      -> EXTRACT     ( m_sq )
#      -> m_or
# ----------------------------

def p_m_sq_m_opt_scope_or_skip_final(p):
    """m_sq : m_opt_scope
            | skip"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_m_sq_m_opt_scope_or_skip(p):
    """m_sq : m_opt_scope m_sq
            | skip m_sq"""
    if isinstance(p[2], list):
        p[0] = [p[1], *p[2]]
    else:
        p[0] = [p[1], p[2]]


def p_m_sq_extract(p):
    """m_sq : EXTRACT '(' m_sq ')'"""
    p[0] = ExtractNode(parse_tree=p[3])


def p_m_sq_m_or(p):
    """m_sq : m_or"""
    p[0] = OrNode(parse_tree=p[1])


# ============================
# m_or -> ( m_sq ) OR ( m_sq )
#      -> ( m_sq ) OR ( m_or )
# ----------------------------
def p_m_or_m_sqs(p):
    """m_or : '(' m_sq ')' OR '(' m_sq ')'"""
    if isinstance(p[2], list) and isinstance(p[6], list):
        p[0] = [*p[2], *p[6]]
    elif isinstance(p[2], list):
        p[0] = [*p[2], p[6]]
    elif isinstance(p[6], list):
        p[0] = [p[2], *p[6]]
    else:
        p[0] = [p[2], p[6]]


def p_m_or_m_sq_m_or(p):
    """m_or : '(' m_sq ')' OR '(' m_or ')'"""
    p[0] = [p[2], *p[6]]


# ============================
# skip -> SKIP _integer_
# ----------------------------
def p_skip(p):
    """skip : SKIP NUMBER"""
    p[0] = SkipNode(skip=p[2])


# ============================
# m_opt_scope -> match
#             -> match WITHIN _integer_
#             -> match BETWEEN _integer_ _integer_
# ----------------------------
def p_m_opt_scope_no_scope(p):
    """m_opt_scope : match"""
    p[0] = p[1]


def p_m_opt_scope_within(p):
    """m_opt_scope : match WITHIN NUMBER"""
    p[0] = WithinNode(parse_tree=p[1], end=p[3])


def p_m_opt_scope_between(p):
    """m_opt_scope : match BETWEEN NUMBER NUMBER"""
    p[0] = BetweenNode(parse_tree=p[1], lower=p[3], upper=p[4])


# ============================
# match -> kind is_op   _string_
#       -> kind like_op _string_
#       -> kind in_op   [ list ]
# ----------------------------
def p_match_is_or_like_ops(p):
    """match : kind is_op STRING
             | kind like_op STRING"""
    p[0] = MatchNode(prop=p[1], op=p[2], value=p[3])


def p_match_in_op(p):
    """match : kind in_op '[' string_list ']'"""
    p[0] = MatchNode(prop=p[1], op=p[2], value=p[4])


# ============================
# is_op -> IS
#       -> IS NOT
#       -> IS NOCASE
#       -> IS NOT NOCASE
# ----------------------------
def p_is_op_is(p):
    """is_op : IS"""
    p[0] = OpNode(op='is')


def p_is_op_is_not(p):
    """is_op : IS NOT"""
    p[0] = OpNode(op='is', has_not=True)


def p_is_op_is_nocase(p):
    """is_op : IS NOCASE"""
    p[0] = OpNode(op='is', no_case=True)


def p_is_op_is_not_nocase(p):
    """is_op : IS NOT NOCASE"""
    p[0] = OpNode(op='is', has_not=True, no_case=True)


# ============================
# in_op -> IN
#       -> NOT IN
#       -> IN NOCASE
#       -> NOT IN NOCASE
# ----------------------------
def p_in_op_in(p):
    """in_op : IN"""
    p[0] = OpNode(op='in')


def p_in_op_not_in(p):
    """in_op : NOT IN"""
    p[0] = OpNode(op='in', has_not=True)


def p_in_op_in_nocase(p):
    """in_op : IN NOCASE"""
    p[0] = OpNode(op='in', no_case=True)


def p_in_op_not_in_nocase(p):
    """in_op : NOT IN NOCASE"""
    p[0] = OpNode(op='in', has_not=True, no_case=True)


# ============================
# like_op -> LIKE
#         -> NOT LIKE
# ----------------------------
def p_like_op(p):
    """like_op : LIKE"""
    p[0] = OpNode(op='like')


def p_like_op_not(p):
    """like_op : NOT LIKE"""
    p[0] = OpNode(op='like', has_not=True)


# ============================
# kind -> VECTOR . _string_
# ----------------------------
def p_kind(p):
    """kind : VECTOR '.' STRING"""
    p[0] = PropertyNode(name=p[3])


# ============================
# list -> _string_
#      -> _string_ , list
# ----------------------------
def p_string_list_first(p):
    """string_list : STRING"""
    p[0] = [p[1]]


def p_string_list(p):
    """string_list : string_list ',' STRING"""
    p[0] = [*p[1], p[3]]


parser = yacc.yacc(debug=True)
