import ply.yacc as yacc

from vpml.vpml_lexer import VpmlLexer

tokens = VpmlLexer.tokens


# ============================
# root -> START m_sq END
# -> START m_sq
# ->       m_sq END
# ->       m_sq
# ----------------------------
def p_root_start_end(p):
    """root : START m_sq END"""
    p[0] = {'start_end', p[2]}


def p_root_start(p):
    """root : START m_sq"""
    p[0] = {'start', p[2]}


def p_root_end(p):
    """root : m_sq END"""
    p[0] = {'end', p[2]}


def p_root_no_start_end(p):
    """root : m_sq """
    p[0] = {'no_start_end', p[2]}


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
    p[0] = p[1]


def p_m_sq_m_opt_scope_or_skip(p):
    """m_sq : m_opt_scope m_sq
            | skip m_sq"""
    p[0] = [p[1], *p[2]]


def p_m_sq_extract(p):
    """m_sq : EXTRACT '(' m_sq ')'"""
    p[0] = {'extract', p[3]}


def p_m_sq_m_or(p):
    """m_sq : m_or"""
    p[0] = {'or', p[1]}


# ============================
# m_or -> ( m_sq ) OR ( m_sq )
#      -> ( m_sq ) OR ( m_or )
# ----------------------------
def p_m_or_m_sqs(p):
    """m_or : '(' m_sq ')' OR '(' m_sq ')'"""
    p[0] = [p[2], p[6]]


def p_m_or_m_sq_m_or(p):
    """m_or :  '(' m_sq ')' OR '(' m_or ')'"""
    p[0] = [p[2], *p[6]]


# ============================
# skip -> SKIP _integer_
# ----------------------------
def p_skip(p):
    """skip: SKIP NUMBER"""
    p[0] = {'skip', p[2]}


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
    p[0] = {'within', p[3], p[1]}

def p_m_opt_scope_between(p):
    """m_opt_scope : match BETWEEN NUMBER NUMBER"""
    p[0] = {'between', p[3], p[4], p[1]}


# ============================
# match -> kind is_op   _string_
#       -> kind like_op _string_
#       -> kind in_op   [ list ]
# ----------------------------
def p_match_is_or_like_ops(p):
    """match : kind is_op STRING
             ¦ kind like_op STRING"""
    p[0] = {p[2], p[1], p[3]}


def p_match_in_op(p):
    """match : kind in_op '[' list ']'"""
    p[0] = {p[2], p[1], p[4]}


# ============================
# is_op -> IS
#       -> IS NOT
#       -> IS NOCASE
#       -> IS NOT NOCASE
# ----------------------------
def p_is_op(p):
    pass # FIXME TODO continue from here

# ============================
# in_op -> IN
#       -> NOT IN
#       -> IN NOCASE
#       -> NOT IN NOCASE
# ----------------------------

# ============================
# like_op -> LIKE
#         -> NOT LIKE
# ----------------------------

def p_string_list(p):
    """string_list : '(' strings ')'"""
    p[0] = p[2]


def p_strings_first(p):
    """strings : STRING"""
    p[0] = [p[1]]


def p_strings(p):
    """strings : strings ',' STRING"""
    p[0] = [*p[1], p[3]]


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
