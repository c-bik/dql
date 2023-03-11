from vpml.vpml_lexer import VpmlLexer
from vpml.vpml_parser import parser


class TestVpmlParser:
    def setup_class(self):
        self.vpml = VpmlLexer()

    def test_start_end(self):
        assert {
                   "root": {
                       "has_end": False,
                       "has_start": False,
                       "parse_tree": [{"skip": 10}]
                   }
               } == parser.parse("SKIP 10", lexer=self.vpml.lexer).to_dict()
        assert {
                   "root": {
                       "has_end": False,
                       "has_start": True,
                       "parse_tree": [{"skip": 10}]
                   }
               } == parser.parse("START SKIP 10", lexer=self.vpml.lexer).to_dict()
        assert {
                   "root": {
                       "has_end": True,
                       "has_start": False,
                       "parse_tree": [{"skip": 10}]
                   }
               } == parser.parse("SKIP 10 END", lexer=self.vpml.lexer).to_dict()
        assert {
                   "root": {
                       "has_end": True,
                       "has_start": True,
                       "parse_tree": [{"skip": 10}]
                   }
               } == parser.parse("START SKIP 10 END", lexer=self.vpml.lexer).to_dict()

    def test_ops(self):
        assert {
                   'match': {
                       'op': {
                           'has_not': False,
                           'no_case': False,
                           'op': 'like'
                       },
                       'property': 'foo',
                       'value': '.*baz'
                   }
               } == parser.parse(
            'VECTOR.foo LIKE ".*baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]
        assert {
                   'has_not': True,
                   'no_case': False,
                   'op': 'like'
               } == parser.parse(
            'VECTOR.foo NOT LIKE ".*baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': False,
                   'no_case': False,
                   'op': 'is'
               } == parser.parse(
            'VECTOR.foo IS "baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': True,
                   'no_case': False,
                   'op': 'is'
               } == parser.parse(
            'VECTOR.foo IS NOT "baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': False,
                   'no_case': True,
                   'op': 'is'
               } == parser.parse(
            'VECTOR.foo IS NOCASE "baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': True,
                   'no_case': True,
                   'op': 'is'
               } == parser.parse(
            'VECTOR.foo IS NOT NOCASE "baz"',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]

        assert {
                   'match': {
                       'op': {
                           'has_not': False,
                           'no_case': False,
                           'op': 'in'
                       },
                       'property': 'foo',
                       'value': ["foo", "bar", "baz"]
                   }
               } == parser.parse(
            'VECTOR.foo IN ["foo", "bar", "baz"]',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]
        assert {
                   'has_not': True,
                   'no_case': False,
                   'op': 'in'
               } == parser.parse(
            'VECTOR.foo NOT IN ["foo", "bar", "baz"]',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': False,
                   'no_case': True,
                   'op': 'in'
               } == parser.parse(
            'VECTOR.foo IN NOCASE ["foo", "bar", "baz"]',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]
        assert {
                   'has_not': True,
                   'no_case': True,
                   'op': 'in'
               } == parser.parse(
            'VECTOR.foo NOT IN NOCASE ["foo", "bar", "baz"]',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"][0]["match"]["op"]

    def test_ands(self):
        assert [
                   {'skip': 10},
                   {
                       'match': {
                           'op': {
                               'has_not': False,
                               'no_case': False,
                               'op': 'is'
                           },
                           'property': 'foo',
                           'value': 'bar'
                       }
                   }
               ] == parser.parse(
            '''
            SKIP 10
            VECTOR.foo is "bar"
            ''',
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"]

        assert {
                   'root': {
                       'has_end': False,
                       'has_start': True,
                       'parse_tree': [
                           {'skip': 10},
                           {
                               'match': {
                                   'op': {
                                       'has_not': False,
                                       'no_case': False,
                                       'op': 'is'
                                   },
                                   'property': 'type',
                                   'value': 'foo'
                               }
                           }
                       ]
                   }
               } == parser.parse(
            '''
            START
            SKIP 10
            VECTOR.type is "foo"
            ''',
            lexer=self.vpml.lexer
        ).to_dict()

    def test_ors(self):
        assert [
                   {'match': {
                       'op': {'has_not': False, 'no_case': False, 'op': 'like'},
                       'property': 'VALUE',
                       'value': '.*foo'}},
                   {'match': {
                       'op': {'has_not': False, 'no_case': False, 'op': 'is'},
                       'property': 'type',
                       'value': 'FOO'}},
                   {'skip': 10},
                   {'or': {'parse_tree': [
                       {'within': {
                           'end': 3,
                           'parse_tree': {'match': {
                               'op': {'has_not': False, 'no_case': False, 'op': 'is'},
                               'property': 'value',
                               'value': 'bar'
                           }}}},
                       {'match': {'op': {'has_not': True, 'no_case': False, 'op': 'in'},
                                  'property': 'type',
                                  'value': ['FOO', 'BAR', 'BAZ']}},
                       {'match': {'op': {'has_not': True, 'no_case': False, 'op': 'in'},
                                  'property': 'type',
                                  'value': ['FOO', 'BAR', 'BAZ']}}
                   ]}}
               ] == parser.parse(
            """
            VECTOR.VALUE LIKE ".*foo"
            VECTOR.type IS "FOO"
            SKIP 10
            (
                VECTOR.value IS "bar" WITHIN 3
                VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
            )
            OR
            ( VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ] )
            """,
            lexer=self.vpml.lexer
        ).to_dict()["root"]["parse_tree"]
