# DQL: Document Query Language

A query language capable of searching a pattern in a sequence of `[..., ("Value", Type), ...]` and select/return a sub pattern if matched. This is built on top of PCRE regex standard hence any literal `"Value"` should be regex able as well.

### Operators
#### Scoping
```
^       : match from the beginning
$       : match from the end
*       : match zero or more
+       : match 1 or more
|       : regex like OR branching
&       : regex like AND combiner
{n,m}   : n < m, n > 0 match atleast n and at most m times
{m}     : match exactly m times
TYPE    : type of an entity
VALUE   : value of an entity
=       : exact equality
!=      : exact inquality
~=      : match with a PCRE regex
!~=     : exclude a PCRE regex match 
```

#### Grouping and selection
```
(...)      : match a group
[...]      : select this match
```

### Examples
Description|Query
---|---
match from the beginning one or more `X` type entities must preceed exactly two `Y` values and followed by exactly one type `A` select two `Y` values (if found)|`^(TYPE="X")+[(VALUE="Y"){2}](TYPE="A")`
