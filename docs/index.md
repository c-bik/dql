# Language definition 

## Definition of components
| Term                        | Definition                                                                                               | Example                                                    |
|-----------------------------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| `TOKEN._string_`            | Match _string_ property part of the vector                                                               | `TOKEN.type LIKE ".*try$"`                                 |
| `SKIP #n`                   | Skip _n_ number of vectors                                                                               | `SKIP 30` skips maximum 30 vectors from current location   |
| `^`                         | Start at the beginning of the vector list                                                                | `^ TOKEN.value IS "India"`<br>`^ TOKEN.type IS "Currency"` |
| `$`                         | Until the end of the vector list                                                                         | `TOKEN.type IS "Type-1" $`<br>`TOKEN.value LIKE "a.*b" $`  |
| `IS`                        | Token or value is exactly same as the target                                                             | `TOKEN.value IS "sunset"`                                  |
| `IN`                        | Token or value is found in the list of targets                                                           | `TOKEN.type IN [ "Currency", "Duration" ]`                 |
| `NOCASE`                    | `IS` or `IN` operators does a case sensitive match by default, this optional modifier can override that  | `TOKEN.value IS NOCASE "iNdiA"`                            |
| `LIKE`                      | Token or value matches target regular expression                                                         | `TOKEN.value LIKE "Coun.*"`                                |
| `NOT`                       | Reverses the `IS` / `IN` / `LIKE` operation outcome                                                      | `IS NOT`<br>`NOT IN`<br>`NOT LIKE`                         |
| `OR`                        | Between either of the two match sequences                                                                | `( ( TOKEN.type IS "a" ) OR ( TOKEN.value IS "b" ) )`      |
| `WITHIN #n`                 | The match must be found within _n_ `(> 0)` vectors                                                       | `TOKEN.value IS "f" WITHIN 10`                             |
| `BETWEEN #n #m`             | The match must be found after _n_<sup>th</sup> and before _m_<sup>th</sup> vector                        | `TOKEN.value IS "x" BETWEEN 5 10`                          |
| `EXTRACT(_match_sequence_)` | The matched sequence will be given as output                                                             | `EXTRACT(TOKEN.value IS "India")`                          |

## Examples _**TBD**_
1. **Check if the text contains a string "foo bar"**
    ```
    ```

## Formal Grammar Specification
```
dql -> ^ m_sq $
    -> ^ m_sq
    ->   m_sq $
    ->   m_sq

m_sq -> match_opt_scope
     -> skip
     -> match_opt_scope m_sq
     -> skip            m_sq
     -> EXTRACT       ( m_sq )
     -> ( m_or )

m_or -> ( m_sq ) OR ( m_sq )
     -> ( m_sq ) OR ( m_or )

skip -> SKIP _integer_

match_opt_scope -> match
                -> match WITHIN _integer_
                -> match BETWEEN _integer_ _integer_

match -> kind is_op    _string_
      -> kind in_op    [ list ]
      -> kind LIKE     _string_
      -> kind NOT LIKE _string_

is_op -> IS
      -> IS NOT
      -> IS NOCASE
      -> IS NOT NOCASE

in_op -> IN
      -> NOT IN
      -> IN NOCASE
      -> NOT IN NOCASE

kind -> TOKEN . _string_

list -> _string_
     -> _string_ , list
```
