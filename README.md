# VPML: Vector Pattern Matcher Language (VP-ML)
[![Build and docs](https://github.com/c-bik/vpml/actions/workflows/ci-docs.yml/badge.svg?branch=main)](https://github.com/c-bik/vpml/actions/workflows/ci-docs.yml)

A query language capable of searching a pattern in a sequence of vectors same cardinality `[..., (value="Value", type=Type, ...), ...]` and select/return a sub pattern if matched. This is built on top of PCRE regex standard hence any literal `"Value"` should be regex able as well.
