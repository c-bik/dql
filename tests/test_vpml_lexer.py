from vpml.vpml_lexer import VpmlLexer


def test_lexer():

    vpml = VpmlLexer()

    expected_tokens = {*vpml.literals, *vpml.tokens}
    expected_tokens.remove('ID')
    expected_tokens = sorted(expected_tokens)

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
                    EXTRACT ( VECTOR.VALUE IN ("foo", "bar", "baz") )
                    VECTOR.VALUE IN ("foo1", "bar1", "baz1")
                )
            ) BETWEEN 3 5
        )
        OR (
            VECTOR.VALUE LIKE ".*foo"
            VECTOR.VALUE IN ("foo1", "bar1", "baz1")
        )
    )
    END
    """)

    # for t in vpml.lexer:
    #     print(t)

    got_tokens = sorted(set(token.type for token in vpml.lexer))

    assert got_tokens == expected_tokens
