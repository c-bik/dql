# VPML Parse tree example
A VPML expression like the following...
```
START
VECTOR.VALUE LIKE ".*foo"
VECTOR.type IS "FOO"
SKIP 10
(
    VECTOR.value IS "bar" WITHIN 3
    VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ]
)
OR
( VECTOR.type NOT IN [ "FOO", "BAR", "BAZ" ] )
END
```
...will produce a parse tree like...
```json
{"root": {"has_end": true, "has_start": true, "parse_tree": [
   {"match": {
      "op": {"has_not": false, "no_case": false, "op": "like"},
      "property": "VALUE",
      "value": ".*foo"}},
   {"match": {
      "op": {"has_not": false, "no_case": false, "op": "is"},
      "property": "type",
      "value": "FOO"}},
   {"skip": 10},
   {"or": {"parse_tree": [
      {"within": {
         "end": 3,
         "parse_tree": {"match": {
            "op": {"has_not": false, "no_case": false, "op": "is"},
            "property": "value",
            "value": "bar"}}}},
      {"match": {
         "op": {"has_not": true, "no_case": false, "op": "in"},
         "property": "type",
         "value": ["FOO", "BAR", "BAZ"]}},
      {"match": {
         "op": {"has_not": true, "no_case": false, "op": "in"},
         "property": "type",
         "value": ["FOO", "BAR", "BAZ"]}}
   ]}}
]}}
```


# Language specification

## Phrases and Keywords
| Term                        | Definition                                                                                               | Example                                                          |
|-----------------------------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| `VECTOR._string_`           | Match _string_ property part of the vector                                                               | `VECTOR.type LIKE ".*try$"`                                      |
| `SKIP #n`                   | Skip _n_ number of vectors                                                                               | `SKIP 30` skips maximum 30 vectors from current location         |
| `START`                     | Start at the beginning of the vector list                                                                | `START VECTOR.value IS "India"`<br>`^ VECTOR.type IS "Currency"` |
| `END`                       | Until the end of the vector list                                                                         | `VECTOR.type IS "Type-1" $`<br>`VECTOR.value LIKE "a.*b" END`    |
| `IS`                        | Token or value is exactly same as the target                                                             | `VECTOR.value IS "sunset"`                                       |
| `IN`                        | Token or value is found in the list of targets                                                           | `VECTOR.type IN [ "Currency", "Duration" ]`                      |
| `NOCASE`                    | `IS` or `IN` operators does a case sensitive match by default, this optional modifier can override that  | `VECTOR.value IS NOCASE "iNdiA"`                                 |
| `LIKE`                      | Token or value matches target regular expression                                                         | `VECTOR.value LIKE "Coun.*"`                                     |
| `NOT`                       | Reverses the `IS` / `IN` / `LIKE` operation outcome                                                      | `IS NOT`<br>`NOT IN`<br>`NOT LIKE`                               |
| `OR`                        | Between either of the two match sequences                                                                | `( ( VECTOR.type IS "a" ) OR ( VECTOR.value IS "b" ) )`          |
| `WITHIN #n`                 | The match must be found within _n_ `(> 0)` vectors                                                       | `VECTOR.value IS "f" WITHIN 10`                                  |
| `BETWEEN #n #m`             | The match must be found after _n_<sup>th</sup> and before _m_<sup>th</sup> vector                        | `VECTOR.value IS "x" BETWEEN 5 10`                               |
| `EXTRACT(_match_sequence_)` | The matched sequence will be given as output                                                             | `EXTRACT(VECTOR.value IS "India")`                               |


## LALR Grammar
```
root -> START m_sq END
     -> START m_sq
     ->       m_sq END
     ->       m_sq

m_sq -> m_opt_scope
     -> skip
     -> m_opt_scope m_sq
     -> skip        m_sq
     -> EXTRACT     ( m_sq )
     -> m_or

m_or -> ( m_sq ) OR ( m_sq )
     -> ( m_sq ) OR ( m_or )

skip -> SKIP _integer_

m_opt_scope -> match
            -> match WITHIN _integer_
            -> match BETWEEN _integer_ _integer_

match -> kind is_op   _string_
      -> kind in_op   [ string_list ]
      -> kind like_op _string_

is_op -> IS
      -> IS NOT
      -> IS NOCASE
      -> IS NOT NOCASE

in_op -> IN
      -> NOT IN
      -> IN NOCASE
      -> NOT IN NOCASE

like_op -> LIKE
        -> NOT LIKE

kind -> VECTOR . _string_

string_list -> _string_
            -> _string_ , string_list
```
