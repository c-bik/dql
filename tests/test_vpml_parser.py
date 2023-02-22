from vpml.vpml_lexer import VpmlLexer
from vpml.vpml_parser import parser


def test_parser():
    vpml = VpmlLexer()

    # vpml_rule = """START
    # VECTOR.type IS "FOO"
    # VECTOR.value IS "bar" WITHIN 3
    # SKIP 10
    # (
    #     (
    #         VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
    #         (
    #             (
    #                 VECTOR.TYPE IN NOCASE ("FOO1", "BAR1", "BAZ1")
    #             ) OR (
    #                 EXTRACT ( VECTOR.VALUE IN ("foo", "bar", "baz") )
    #                 VECTOR.VALUE IN ("foo1", "bar1", "baz1")
    #             )
    #         ) BETWEEN 3 5
    #     )
    #     OR (
    #         VECTOR.VALUE LIKE ".*foo"
    #         VECTOR.VALUE IN ("foo1", "bar1", "baz1")
    #     )
    # )
    # END"""
    vpml_rule = """
    START
    VECTOR.VALUE LIKE ".*foo"
    VECTOR.type IS "FOO"
    VECTOR.value IS "bar" WITHIN 3
    VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
    SKIP 10
    END
    """

    rule = parser.parse(vpml_rule, lexer=vpml.lexer)
    print(rule)

    # expected_rule = [
    #    ('type', 'FOO'),
    #    ('before', 3, ('value', 'bar')),
    #    ('skip', 10),
    #    ('after', 5,
    #     ('or', [
    #         [
    #             ('type', ['FOO', 'BAR', 'BAZ']),
    #             ('between', 3, 5,
    #              ('or', [
    #                  ('type', ['FOO1', 'BAR1', 'BAZ1']),
    #                  [
    #                      ('value', ['foo', 'bar', 'baz']),
    #                      ('value', ['foo1', 'bar1', 'baz1'])
    #                  ],
    #                  [
    #                      ('value', ['foo2', 'bar2', 'baz2']),
    #                      ('value', ['foo3', 'bar3', 'baz3'])
    #                  ]
    #              ]))
    #         ],
    #         [
    #             ('value', ['foo', 'bar', 'baz']),
    #             ('value', ['foo1', 'bar1', 'baz1'])
    #         ],
    #         [
    #             ('value', ['foo2', 'bar2', 'baz2']),
    #             ('value', ['foo3', 'bar3', 'baz3'])
    #         ]
    #     ]))
    # ]

    # assert expected_rule == rule
