from pprint import pprint

from dql.dql_lex import DqlLex
from dql.dql_yac import parser

input_string = """
TYPE IS "FOO"
VALUE IS "bar" WITHIN MAX 3
(
    TYPE IN ("FOO", "BAR", "BAZ")
    OR VALUE IN ("foo", "bar", "baz")
) WITHIN MAX 5
"""


def test_lexer():
    dq = DqlLex()
    dq.tokenize(input_string=input_string)

    expected = [
        ('TYPE', 'TYPE'),
        ('IS', 'IS'),
        ('STRING', 'FOO'),
        ('VALUE', 'VALUE'),
        ('IS', 'IS'),
        ('STRING', 'bar'),
        ('WITHIN', 'WITHIN'),
        ('MAX', 'MAX'),
        ('NUMBER', 3),
        ('(', '('),
        ('TYPE', 'TYPE'),
        ('IN', 'IN'),
        ('(', '('),
        ('STRING', 'FOO'),
        (',', ','),
        ('STRING', 'BAR'),
        (',', ','),
        ('STRING', 'BAZ'),
        (')', ')'),
        ('OR', 'OR'),
        ('VALUE', 'VALUE'),
        ('IN', 'IN'),
        ('(', '('),
        ('STRING', 'foo'),
        (',', ','),
        ('STRING', 'bar'),
        (',', ','),
        ('STRING', 'baz'),
        (')', ')'),
        (')', ')'),
        ('WITHIN', 'WITHIN'),
        ('MAX', 'MAX'),
        ('NUMBER', 5)
    ]

    actual = [
        (tok.type, tok.value)
        for tok in dq.lexer
    ]

    assert expected == actual


def test_parser():
    dq = DqlLex()
    input_string1 = """
    TYPE IS "FOO"
    VALUE IS "bar" WITHIN MAX 3
    (
        TYPE IN ("FOO", "BAR", "BAZ")
        OR VALUE IN ("foo", "bar", "baz")
    ) WITHIN MAX 5
    """
    p = parser.parse(input_string1, lexer=dq.lexer)
    print()
    pprint(p)
