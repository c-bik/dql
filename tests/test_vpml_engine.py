from vpml.vpml_engine import VpmlEngine
from vpml.vpml_lexer import VpmlLexer
from vpml.vpml_parser import parser


class TestVpmlEngine:
    def setup_class(self):
        self.vpml = VpmlLexer()

    def test_first_match(self):
        match_result = VpmlEngine(
            vpml=parser.parse(
                """
                VECTOR.VALUE LIKE ".*foo"
                VECTOR.type IS "FOO"
                SKIP 1
                (
                    VECTOR.value IS "bar" WITHIN 3
                    VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
                )
                OR
                ( VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ] )
                """,
                lexer=self.vpml.lexer
            )
        ).match(
            [
                {"value": "bar foo", "type": "type1"},
                {"value": "bar foo", "type": "FOO"},
                {"value": "bar foo", "type": "FOO1"},
                {"value": "bar", "type": "FOO1"},
                {"value": "bar", "type": "FOO1"},
            ]
        )
        print("")
        print(match_result)
