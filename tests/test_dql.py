from vpml.lexer import DqlLex
from vpml.parser import parser
from vpml.engine import DqlEngine


def test_parser():
    dq = DqlLex()
    dql = """
    TYPE IS "FOO"
    VALUE IS "bar" BEFORE 3
    SKIP 10
    (
        (
            TYPE IN ("FOO", "BAR", "BAZ")
            (
                TYPE IN ("FOO1", "BAR1", "BAZ1")
                OR (
                    VALUE IN ("foo", "bar", "baz")
                    VALUE IN ("foo1", "bar1", "baz1")
                )
                OR (
                    VALUE IN ("foo2", "bar2", "baz2")
                    VALUE IN ("foo3", "bar3", "baz3")
                )
            ) BETWEEN 3 5
        )
        OR (
            VALUE IN ("foo", "bar", "baz")
            VALUE IN ("foo1", "bar1", "baz1")
        )
        OR (
            VALUE IN ("foo2", "bar2", "baz2")
            VALUE IN ("foo3", "bar3", "baz3")
        )
    ) AFTER 5
    """

    rule = parser.parse(dql, lexer=dq.lexer)

    expected_rule = [
        ('type', 'FOO'),
        ('before', 3, ('value', 'bar')),
        ('skip', 10),
        ('after', 5,
         ('or', [
             [
                 ('type', ['FOO', 'BAR', 'BAZ']),
                 ('between', 3, 5,
                  ('or', [
                      ('type', ['FOO1', 'BAR1', 'BAZ1']),
                      [
                          ('value', ['foo', 'bar', 'baz']),
                          ('value', ['foo1', 'bar1', 'baz1'])
                      ],
                      [
                          ('value', ['foo2', 'bar2', 'baz2']),
                          ('value', ['foo3', 'bar3', 'baz3'])
                      ]
                  ]))
             ],
             [
                 ('value', ['foo', 'bar', 'baz']),
                 ('value', ['foo1', 'bar1', 'baz1'])
             ],
             [
                 ('value', ['foo2', 'bar2', 'baz2']),
                 ('value', ['foo3', 'bar3', 'baz3'])
             ]
         ]))
    ]
    assert expected_rule == rule


def test_engine():
    dq = DqlLex()
    input_string1 = """
    TYPE IS "FOO"
    VALUE IS "bar" BEFORE 3
    SKIP 1
    TYPE IS "d" AFTER 1
    """
    rules = parser.parse(input_string1, lexer=dq.lexer)

    tokens = [('FOO', 1), ('FOO', "bar"), ('b', 2), ('d', 5)]
    assert not DqlEngine(rules).match(tokens)
