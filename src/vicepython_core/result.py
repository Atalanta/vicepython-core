"""Helper functions for working with Result types.

All functions use structural pattern matching and are pure (no side effects).
Import these explicitly: `from vicepython_core.result import map_ok, and_then, collect`
"""

from collections.abc import Callable, Sequence

from vicepython_core.types import Err, Ok, Result


def map_ok[T, U, E](result: Result[T, E], f: Callable[[T], U]) -> Result[U, E]:
    """Apply a function to the value inside Ok, leaving Err unchanged.

    Args:
        result: The Result to map over
        f: Function to apply to the Ok value

    Returns:
        Result[U, E]: Ok with transformed value, or original Err
    """
    match result:
        case Ok(value):
            return Ok(f(value))
        case Err():
            return result


def and_then[T, U, E](result: Result[T, E], f: Callable[[T], Result[U, E]]) -> Result[U, E]:
    """Chain a Result-returning function, short-circuiting on Err.

    Also known as flatMap or bind in other languages.

    Args:
        result: The Result to chain from
        f: Function that returns a new Result

    Returns:
        Result[U, E]: Result from applying f, or original Err
    """
    match result:
        case Ok(value):
            return f(value)
        case Err():
            return result


def collect[T, E](results: Sequence[Result[T, E]]) -> Result[list[T], E]:
    """Collect a sequence of Results into a single Result containing a list.

    Fail-fast: returns the first Err encountered, or Ok with all values.
    Edge case: collect([]) returns Ok([]).

    Args:
        results: Sequence of Results to collect

    Returns:
        Result[list[T], E]: Ok with list of all values, or first Err

    Example:
        >>> collect([Ok(1), Ok(2), Ok(3)])
        Ok([1, 2, 3])
        >>> collect([Ok(1), Err("bad"), Ok(3)])
        Err("bad")
        >>> collect([])
        Ok([])
    """
    collected_values: list[T] = []

    for result in results:
        match result:
            case Ok(value):
                collected_values.append(value)
            case Err():
                return result

    return Ok(collected_values)
