import re
from pprint import pprint

from ply import lex
from ply.lex import TOKEN


class VpmlLexer:
    reserved = [
        'START',
        'END',
        'VECTOR',
        'SKIP',
        'IS',
        'IN',
        'NOCASE',
        'LIKE',
        'NOT',
        'OR',
        'WITHIN',
        'BETWEEN',
        'EXTRACT'
    ]

    literals = "().[],"

    tokens = ['NUMBER', 'STRING', 'ID', *reserved]

    t_ignore = ' \t'

    t_ignore_COMMENT = r'\#.*'

    @TOKEN(r'((?<![\\])")((?:.(?!(?<![\\])"))*.?)"')
    def t_STRING(self, t):
        t.value = re.search(r'"([^"]+)"', t.value).group(1)
        return t

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize(self, input_string: str):
        self.lexer.input(input_string)

    # Define a rule so we can track line numbers
    @TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    @TOKEN(r'[^".][a-zA-Z]+')
    def t_ID(self, t):
        t.value = t.value.upper()
        if t.value in self.reserved:
            t.type = t.value
        else:
            t.type = 'STRING'
        return t

    @TOKEN(r'\d+')
    def t_NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def test(self, data):
        self.tokenize(data)
        for token in self.lexer:
            print(token)


if __name__ == '__main__':
    vpml = VpmlLexer()
    vpml.test('VECTOR.type like "^.*foo{VECTOR.type2,3}+([^bar.*\\\"]).*$"')
