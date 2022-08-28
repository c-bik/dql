import re

from ply import lex

tokens = (
    'START',
    'END',
    'MATCH',
    'WHEN',
    'SENTENCE',
    'PARAGRAPH',
    'TYPE',
    'VALUE',
    'IS',
    'LIKE',
    'LPAREN',
    'RPAREN',
    'IN',
    'COMMA',
    'MATCHES',
    'OR',
    'SELECT',
    'WITHIN',
    'MAX',
    'NUMBER',
    'STRING',
)

t_ignore = ' \t'

t_START = r'START|start'
t_END = r'END|end'
t_MATCH = r'MATCH|match'
t_WHEN = r'WHEN|when'
t_SENTENCE = r'SENTENCE|sentence'
t_PARAGRAPH = r'PARAGRAPH|paragraph'
t_TYPE = r'TYPE|type'
t_VALUE = r'VALUE|value'
t_IS = r'IS|is'
t_LIKE = r'LIKE|like'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IN = r'IN'
t_COMMA = r'\,'
t_MATCHES = r'MATCHES|matches'
t_OR = r'OR|or'
t_SELECT = r'SELECT|select'
t_WITHIN = r'WITHIN|within'
t_MAX = r'MAX|max'


def t_STRING(t):
    r'"[^"]+"'
    t.value = re.search(r'"([^"]+)"', t.value).group(1)
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
