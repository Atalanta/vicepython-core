"""Canonical Result and Option types for VicePython.

This package provides algebraic data types for explicit error handling (Result)
and optional values (Option). Helper functions are available in separate modules
and must be imported explicitly.

Example:
    >>> from vicepython_core import Ok, Err, Result, Some, Nothing, Option
    >>> from vicepython_core.result import map_ok, and_then, collect
    >>> from vicepython_core.option import option_from_optional, require_some
"""

from vicepython_core.types import (
    Err,
    JSONValue,
    Nothing,
    Ok,
    Option,
    Result,
    Some,
)

__all__ = [
    "Err",
    "JSONValue",
    "Nothing",
    "Ok",
    "Option",
    "Result",
    "Some",
]
