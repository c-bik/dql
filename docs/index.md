# Language definition 

## Definition of components
| Term            | Definition                                          | Example                                                  |
|-----------------|-----------------------------------------------------|----------------------------------------------------------|
| `TOKEN`         | Match Token part of the vector                      | `TOKEN LIKE ".*try$"`                                    |
| `VALUE`         | Match Value part of the vector                      | `VALUE LIKE ".*try$"`                                    |
| `SKIP #n`       | Skip _n_ number of vectors                          | `SKIP 30` skips maximum 30 vectors from current location |
| `^`             | Beginning of the vector list                        | `^ VALUE IS "India"`<br>`^ TYPE IS "Currency"`           |
| `$`             | End of the vector list                              | `TOKEN IS "Type-1" $`<br>`VALUE LIKE "a.*b" $`           |
| `IS`            | Token or value is exactly same as the target        | `VALUE IS "sunset"`                                      |
| `IN`            | Token or value is found in the list of targets      | `TOKEN IN [ "Currency", "Duration" ]`                    |
| `LIKE`          | Token or value matches target regular expression    | `VALUE LIKE "Coun.*"`                                    |
| `NOT`           | Reverses the `IS` / `IN` / `LIKE` operation outcome | `IS NOT`<br>`NOT IN`<br>`NOT LIKE`                       |
| `OR`            | _**TBD**_                                           |                                                          |
| `BEFORE #n`     | _**TBD**_                                           |                                                          |
| `BETWEEN #n #m` | _**TBD**_                                           |                                                          |


## Formal Grammar Specification
```
dql -> ^ m_sq $
    -> ^ m_sq
    ->   m_sq $
    ->   m_sq

m_sq -> match
     -> skip
     -> match   m_sq
     -> skip    m_sq
     -> EXTRACT ( m_sq )

skip -> SKIP _integer_

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