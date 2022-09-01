

```
OCR -> extracted.json -> tokenize (value, token, lemma) -> apply rules (scope, selection)
         |                                                    |
         \____________________________________________________\__________-> caluse.json / kdp#1.json
``` 



TYPE|VALUE|LEMMA IS|IN|LIKE _string_

LEMMA LIKE "default.*"

```
TYPE IS "FOO"
SKIP MAX 5
VALUE IS "bar" [EXPORT]
LEMMA IS "xyz"
SKIP MAX 6
(
    TYPE IN ( "FOO", "BAR", "BAZ") <-- branch 1
    OR VALUE IN ( "foo", "bar", "baz" ) <-- branch 2
) EXPORT
```
[("bar", _), (_, "FOO")]
[("bar", _), ("bar", _)]

### match brnch 1
value|type
---|---
bla|X
bla2|Y
something|FOO
bar|Z
xzy|BAZ


### match brnch 2
value|type
---|---
bla|X
bla2|Y
something|FOO
bar|Z
baz|W



```
[START]
TYPE IS "FOO"
SKIP MAX 5
VALUE IS "bar"
SKIP MAX 6
(
    TYPE IN ( "FOO", "BAR", "BAZ") <-- branch 1
    OR VALUE IN ( "foo", "bar", "baz" ) <-- branch 2
)
[END]
```
