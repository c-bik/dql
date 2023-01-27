# Language definition 

## Definition of components
| Term            | Definition                                                                        | Example                                                  |
|-----------------|-----------------------------------------------------------------------------------|----------------------------------------------------------|
| `TOKEN`         | Match Token part of the vector                                                    | `TOKEN LIKE ".*try$"`                                    |
| `VALUE`         | Match Value part of the vector                                                    | `VALUE LIKE ".*try$"`                                    |
| `SKIP #n`       | Skip _n_ number of vectors                                                        | `SKIP 30` skips maximum 30 vectors from current location |
| `^`             | Start at the beginning of the vector list                                         | `^ VALUE IS "India"`<br>`^ TYPE IS "Currency"`           |
| `$`             | Until the end of the vector list                                                  | `TOKEN IS "Type-1" $`<br>`VALUE LIKE "a.*b" $`           |
| `IS`            | Token or value is exactly same as the target                                      | `VALUE IS "sunset"`                                      |
| `IN`            | Token or value is found in the list of targets                                    | `TOKEN IN [ "Currency", "Duration" ]`                    |
| `LIKE`          | Token or value matches target regular expression                                  | `VALUE LIKE "Coun.*"`                                    |
| `NOT`           | Reverses the `IS` / `IN` / `LIKE` operation outcome                               | `IS NOT`<br>`NOT IN`<br>`NOT LIKE`                       |
| `OR`            | Between either of the two match sequences                                         | `( ( TOKEN IS "a" ) OR ( VALUE IS "b" ) )`               |
| `WITHIN #n`     | The match must be found within _n_ `(> 0)` vectors                                | `VALIE IS "f" WITHIN 10`                                 |
| `BETWEEN #n #m` | The match must be found after _n_<sup>th</sup> and before _m_<sup>th</sup> vector | `VALUE IS "x" BETWEEN 5 10`                              |


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

match -> kind IS       STRING
      -> kind IS NOT   STRING
      -> kind LIKE     STRING
      -> kind NOT L[mkdocs.yml](..%2Fmkdocs.yml)IKE STRING
      -> kind IN       [ list ]
      -> kind NOT IN   [ list ]

kind -> TOKEN
     -> VALUE

list -> STRING
     -> STRING , list
```