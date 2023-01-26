import ply.yacc as yacc

from dql.lexer import DqlLex

tokens = DqlLex.tokens


def p_root(p):
    """root : dfa"""
    p[0] = p[1]


# string_list : ( strings )
#
# strings     : strings , STRING
# strings     : STRING

def p_string_list(p):
    """string_list : '(' strings ')'"""
    p[0] = p[2]


def p_strings_first(p):
    """strings : STRING"""
    p[0] = [p[1]]


def p_strings(p):
    """strings : strings ',' STRING"""
    p[0] = [*p[1], p[3]]


# dfa : TYPE IS STRING
#     | TYPE IN string_list
#     | TYPE LIKE STRING
#     | VALUE IS STRING
#     | VALUE IN string_list
#     | VALUE LIKE STRING
#     | SKIP NUMBER
#     | ( dfa )
#     | dfa OR dfa
#     | dfa AFTER NUMBER
#     | dfa BEFORE NUMBER
#     | dfa BETWEEN NUMBER NUMBER
#     | dfa dfa

def p_and_dfa(p):
    """dfa : dfa dfa"""
    if isinstance(p[2], list):
        p[0] = [p[1], *p[2]]
    else:
        p[0] = [p[1], p[2]]


def p_or_dfa(p):
    """dfa : dfa OR dfa"""
    if p[3][0] == 'or':
        p[0] = ('or', [p[1], *p[3][1]])
    else:
        p[0] = ('or', [p[1], p[3]])


def p_dfa_in_dfa(p):
    """dfa : '(' dfa ')'"""
    p[0] = (p[2])


def p_dfa_after(p):
    """dfa : dfa AFTER NUMBER"""
    if p[3] < 1:
        raise SyntaxError(f"Invalid value for 'after': {p[3]}, MUST be '> 0'")
    p[0] = ("after", p[3], p[1])


def p_dfa_before(p):
    """dfa : dfa BEFORE NUMBER"""
    if p[3] < 1:
        raise SyntaxError(f"Invalid value for 'before': {p[3]}, MUST be '> 0'")
    p[0] = ("before", p[3], p[1])


def p_dfa_between(p):
    """dfa : dfa BETWEEN NUMBER NUMBER"""
    if p[3] < 1:
        raise SyntaxError(f"Invalid value for 'between' lower bound: {p[2]}, MUST be '> 0'")
    elif p[4] < 1:
        raise SyntaxError(f"Invalid value for 'between' upper bound: {p[3]}, MUST be '> 0'")
    elif p[4] < p[3]:
        raise SyntaxError(f"Invalid values for 'between' range: {p[4]}, MUST be '>' {p[3]}")
    p[0] = ("between", p[3], p[4], p[1])


def p_skip(p):
    """dfa : SKIP NUMBER"""
    if p[2] < 1:
        raise SyntaxError(f"Invalid value for 'skip': {p[2]}, MUST be '> 0'")
    p[0] = ('skip', p[2])


def p_dfa_type_is(p):
    """dfa : TYPE IS STRING"""
    p[0] = ('type', p[3])


def p_dfa_type_in(p):
    """dfa : TYPE IN string_list"""
    p[0] = ('type', p[3])


def p_dfa_type_like(p):
    """dfa : TYPE LIKE STRING"""
    p[0] = ('type', p[3])  # TODO compile regex


def p_dfa_value_is(p):
    """dfa : VALUE IS STRING"""
    p[0] = ('value', p[3])


def p_dfa_value_in(p):
    """dfa : VALUE IN string_list"""
    p[0] = ('value', p[3])


def p_dfa_value_like(p):
    """dfa : VALUE LIKE string_list"""
    p[0] = ('value', p[3])  # TODO compile regex


parser = yacc.yacc()
