import re

from ply import lex

reserved = [
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
    'IN',
    'MATCHES',
    'OR',
    'SELECT',
    'WITHIN',
    'MAX',
]

tokens = [
             'LPAREN',
             'RPAREN',
             'COMMA',
             'NUMBER',
             'STRING',
             'ID',
         ] + reserved

t_ignore = ' \t'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ID(t):
    r'[^"][a-zA-Z]+'
    t.value = t.value.upper()
    if t.value in reserved:
        t.type = t.value
    else:
        raise Exception(f"Unsupported {t}")
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"]+"'
    t.value = re.search(r'"([^"]+)"', t.value).group(1)
    return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
