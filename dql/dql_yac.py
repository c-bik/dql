import ply.yacc as yacc


from dql.dql_lex import DqlLex

tokens = DqlLex.tokens


def p_root(p):
    """root : MATCH scope WHEN dfa SELECT scope"""
    p[0] = {
        "match": p[2],
        "when": p[4],
        "select": p[6]
    }


def p_scope(p):
    """scope : SENTENCE
             | PARAGRAPH"""
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
    p[0] = [p[1].value]


def p_strings(p):
    """strings : strings ',' STRING"""
    p[0] = [*p[1], p[3]]


def p_within(p):
    """within : WITHIN MAX NUMBER"""
    p[0] = {"within", "max", p[3].value}


# dfa : TYPE IS STRING
#     | TYPE IN string_list
#     | TYPE LIKE STRING
#     | VALUE IS STRING
#     | VALUE IN string_list
#     | VALUE LIKE STRING
#     | ( dfa )
#     | dfa OR dfa
#     | dfa within

def p_or_dfa(p):
    """dfa : dfa OR dfa"""
    p[0] = ('or', p[1], p[3])


def p_dfa_in_dfa(p):
    """dfa : '(' dfa ')'"""
    p[0] = (p[2])


def p_dfa_within(p):
    """dfa : dfa within"""
    p[0] = ('within', p[2], p[1])


def p_dfa_type_is(p):
    """dfa : TYPE IS STRING"""
    p[0] = ('type', 'is', p[1])


def p_dfa_type_in(p):
    """dfa : TYPE IN string_list"""
    p[0] = ('type', 'is', p[1])


def p_dfa_type_like(p):
    """dfa : TYPE LIKE string_list"""
    p[0] = ('type', 'like', p[1])  # TODO compile regex


def p_dfa_value_is(p):
    """dfa : VALUE IS STRING"""
    p[0] = ('value', 'is', p[1])


def p_dfa_value_in(p):
    """dfa : VALUE IN string_list"""
    p[0] = ('value', 'is', p[1])


def p_dfa_value_like(p):
    """dfa : VALUE LIKE string_list"""
    p[0] = ('value', 'like', p[1])  # TODO compile regex


parser = yacc.yacc()
