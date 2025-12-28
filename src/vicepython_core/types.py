"""Canonical algebraic data types for VicePython.

This module is the stability anchor of vicepython-core. Changes to these types
are extremely rare and treated as semver-breaking even in 0.x. The types are
pure data containers with no behavioral methods (except __repr__/__str__ for
debugging).

Design Invariant: ADT classes remain pure data containers. No behavioral
methods are permitted. All behavior belongs in free functions in helper modules.

Kind Field Invariant: The 'kind' fields exist solely to support pattern matching
ergonomics and debugging output. They are not part of the semantic API. Never
inspect them directly (e.g., if result.kind == "ok"). Always use pattern matching
to discriminate variants.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Ok[T]:
    """Success variant of Result, containing a success value."""

    value: T
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True)
class Err[E]:
    """Failure variant of Result, containing an error value."""

    error: E
    kind: Literal["err"] = "err"


type Result[T, E] = Ok[T] | Err[E]
"""Result type representing either success (Ok) or failure (Err)."""


@dataclass(frozen=True)
class Some[T]:
    """Presence variant of Option, containing a value."""

    value: T
    kind: Literal["some"] = "some"


@dataclass(frozen=True)
class Nothing:
    """Absence variant of Option, representing no value.

    Note: Nothing() remains constructible; users can create their own
    NOTHING = Nothing() constant if desired, but we don't force a singleton.
    """

    kind: Literal["nothing"] = "nothing"


type Option[T] = Some[T] | Nothing
"""Option type representing either presence (Some) or absence (Nothing)."""


type JSONValue = dict[str, "JSONValue"] | list["JSONValue"] | str | int | float | bool | None
"""Type representing valid JSON values.

Warning: Do not use JSONValue as a lazy domain model. If your domain has
structured data, define proper typed dataclasses. JSONValue is for boundaries
(adapters/ffi) and for data that is genuinely polymorphic/dynamic.
"""
