"""Helper functions for working with Option types.

All functions use structural pattern matching and are pure (no side effects).
Import these explicitly: `from vicepython_core.option import map_some, and_then,
option_from_optional, require_some`
"""

from collections.abc import Callable

from vicepython_core.types import Err, Nothing, Ok, Option, Result, Some


def map_some[T, U](opt: Option[T], f: Callable[[T], U]) -> Option[U]:
    """Apply a function to the value inside Some, leaving Nothing unchanged.

    Args:
        opt: The Option to map over
        f: Function to apply to the Some value

    Returns:
        Option[U]: Some with transformed value, or Nothing
    """
    match opt:
        case Some(value):
            return Some(f(value))
        case Nothing():
            return opt


def and_then[T, U](opt: Option[T], f: Callable[[T], Option[U]]) -> Option[U]:
    """Chain an Option-returning function, short-circuiting on Nothing.

    Also known as flatMap or bind in other languages.

    Args:
        opt: The Option to chain from
        f: Function that returns a new Option

    Returns:
        Option[U]: Option from applying f, or Nothing
    """
    match opt:
        case Some(value):
            return f(value)
        case Nothing():
            return opt


def option_from_optional[T](value: T | None) -> Option[T]:
    """Convert Optional (T | None) to Option[T].

    This is the canonical boundary conversion for external code that uses
    Optional. Convert to Option at boundaries before entering domain code.

    Args:
        value: Optional value to convert

    Returns:
        Option[T]: Some(value) if non-None, Nothing otherwise

    Example:
        >>> option_from_optional(42)
        Some(42)
        >>> option_from_optional(None)
        Nothing()
    """
    if value is None:
        return Nothing()
    return Some(value)


def require_some[T, E](opt: Option[T], err: E) -> Result[T, E]:
    """Convert Option to Result, providing an error for the Nothing case.

    Args:
        opt: The Option to convert
        err: Error value to use if Option is Nothing

    Returns:
        Result[T, E]: Ok with value if Some, Err with provided error if Nothing

    Example:
        >>> require_some(Some(42), "missing value")
        Ok(42)
        >>> require_some(Nothing(), "missing value")
        Err("missing value")
    """
    match opt:
        case Some(value):
            return Ok(value)
        case Nothing():
            return Err(err)
