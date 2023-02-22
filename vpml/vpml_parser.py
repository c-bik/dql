import ply.yacc as yacc

from vpml.vpml_lexer import VpmlLexer

tokens = VpmlLexer.tokens


# ============================
# root -> START m_sq END
#      -> START m_sq
#      ->       m_sq END
#      ->       m_sq
# ----------------------------
def p_root_start_end(p):
    """root : START m_sq END"""
    p[0] = ('start_end', p[2])


def p_root_start(p):
    """root : START m_sq"""
    p[0] = ('start', p[2])


def p_root_end(p):
    """root : m_sq END"""
    p[0] = ('end', p[1])


def p_root_no_start_end(p):
    """root : m_sq"""
    p[0] = ('no_start_end', p[1])


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
    p[0] = [p[1], p[2]]


def p_m_sq_extract(p):
    """m_sq : EXTRACT '(' m_sq ')'"""
    p[0] = ('extract', p[3])


def p_m_sq_m_or(p):
    """m_sq : m_or"""
    p[0] = ('or', p[1])


# ============================
# m_or -> ( m_sq ) OR ( m_sq )
#      -> ( m_sq ) OR ( m_or )
# ----------------------------
def p_m_or_m_sqs(p):
    """m_or : '(' m_sq ')' OR '(' m_sq ')'"""
    p[0] = [p[2], p[6]]


def p_m_or_m_sq_m_or(p):
    """m_or : '(' m_sq ')' OR '(' m_or ')'"""
    p[0] = [p[2], *p[6]]


# ============================
# skip -> SKIP _integer_
# ----------------------------
def p_skip(p):
    """skip : SKIP NUMBER"""
    p[0] = ('skip', p[2])


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
    if p[3] < 1:
        raise SyntaxError(f"Invalid value for 'within': {p[3]}, MUST be '> 0'")
    p[0] = ('within', p[3], p[1])


def p_m_opt_scope_between(p):
    """m_opt_scope : match BETWEEN NUMBER NUMBER"""
    if p[3] < 1:
        raise SyntaxError(f"Invalid value for 'between' lower bound: {p[2]}, MUST be '> 0'")
    elif p[4] < 1:
        raise SyntaxError(f"Invalid value for 'between' upper bound: {p[3]}, MUST be '> 0'")
    elif p[4] < p[3]:
        raise SyntaxError(f"Invalid values for 'between' range: {p[4]}, MUST be '>' {p[3]}")
    p[0] = ('between', p[3], p[4], p[1])


# ============================
# match -> kind is_op   _string_
#       -> kind like_op _string_
#       -> kind in_op   [ list ]
# ----------------------------
def p_match_is_or_like_ops(p):
    """match : kind is_op STRING
             | kind like_op STRING"""
    p[0] = (p[2], p[1], p[3])


def p_match_in_op(p):
    """match : kind in_op '[' list ']'"""
    p[0] = (p[2], p[1], p[4])


# ============================
# is_op -> IS
#       -> IS NOT
#       -> IS NOCASE
#       -> IS NOT NOCASE
# ----------------------------
def p_is_op_is(p):
    """is_op : IS"""
    p[0] = 'is'


def p_is_op_is_not(p):
    """is_op : IS NOT"""
    p[0] = 'is_not'


def p_is_op_is_nocase(p):
    """is_op : IS NOCASE"""
    p[0] = 'is_nocase'


def p_is_op_is_not_nocase(p):
    """is_op : IS NOT NOCASE"""
    p[0] = 'is_not_nocase'


# ============================
# in_op -> IN
#       -> NOT IN
#       -> IN NOCASE
#       -> NOT IN NOCASE
# ----------------------------
def p_in_op_in(p):
    """in_op : IN"""
    p[0] = 'in'


def p_in_op_not_in(p):
    """in_op : NOT IN"""
    p[0] = 'in_not'


def p_in_op_in_nocase(p):
    """in_op : IN NOCASE"""
    p[0] = 'in_nocase'


def p_in_op_not_in_nocase(p):
    """in_op : NOT IN NOCASE"""
    p[0] = 'in_not_nocase'


# ============================
# like_op -> LIKE
#         -> NOT LIKE
# ----------------------------
def p_like_op(p):
    """like_op : LIKE"""
    p[0] = 'like'


def p_like_op_not(p):
    """like_op : NOT LIKE"""
    p[0] = 'like_not'


# ============================
# kind -> VECTOR . _string_
# ----------------------------
def p_kind(p):
    """kind : VECTOR '.' STRING"""
    p[0] = ("property", p[3])


# ============================
# list -> _string_
#      -> _string_ , list
# ----------------------------

def p_list_first(p):
    """list : STRING"""
    p[0] = [p[1]]


def p_list(p):
    """list : list ',' STRING"""
    p[0] = [*p[1], p[3]]


parser = yacc.yacc(debug=True)
