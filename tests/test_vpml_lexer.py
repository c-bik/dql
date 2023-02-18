from vpml.vpml_lexer import VpmlLexer
from vpml.vpml_parser import parser
from vpml.vpml_engine import DqlEngine


def test_lexer():
    vpml = VpmlLexer()
    vpml.tokenize("""
    START
    VECTOR.type IS "FOO"
    VECTOR.value IS "bar" WITHIN 3
    SKIP 10
    (
        (
            VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
            (
                (
                    VECTOR.TYPE IN NOCASE ("FOO1", "BAR1", "BAZ1")
                ) OR (
                    VECTOR.VALUE IN ("foo", "bar", "baz")
                    VECTOR.VALUE IN ("foo1", "bar1", "baz1")
                )
            ) BETWEEN 3 5
        )
        OR (
            VECTOR.VALUE IN ("foo", "bar", "baz")
            VECTOR.VALUE IN ("foo1", "bar1", "baz1")
        )
    )
    END
    """)

    for token in vpml.lexer:
        print(token)
