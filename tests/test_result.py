"""Tests for Result helper functions.

Example tests and hypothesis property tests focusing on practical invariants.
"""

from hypothesis import given
from hypothesis import strategies as st

from vicepython_core import Err, Ok, Result
from vicepython_core.result import and_then, collect, map_ok


# Example tests for map_ok
def test_map_ok_with_ok() -> None:
    """map_ok applies function to Ok value."""
    result: Result[int, str] = Ok(5)
    mapped = map_ok(result, lambda x: x * 2)

    match mapped:
        case Ok(value):
            assert value == 10
        case Err():
            raise AssertionError("Should be Ok")


def test_map_ok_with_err() -> None:
    """map_ok leaves Err unchanged."""
    result: Result[int, str] = Err("error")
    mapped = map_ok(result, lambda x: x * 2)

    match mapped:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "error"


# Example tests for and_then
def test_and_then_with_ok() -> None:
    """and_then chains Ok value through function."""
    result: Result[int, str] = Ok(5)
    chained = and_then(result, lambda x: Ok(x * 2))

    match chained:
        case Ok(value):
            assert value == 10
        case Err():
            raise AssertionError("Should be Ok")


def test_and_then_with_ok_returning_err() -> None:
    """and_then can convert Ok to Err."""
    result: Result[int, str] = Ok(5)
    chained = and_then(result, lambda x: Err("converted to error"))

    match chained:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "converted to error"


def test_and_then_with_err() -> None:
    """and_then leaves Err unchanged."""
    result: Result[int, str] = Err("error")
    chained = and_then(result, lambda x: Ok(x * 2))

    match chained:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "error"


# Example tests for collect
def test_collect_all_ok() -> None:
    """collect returns Ok with list of values when all are Ok."""
    results: list[Result[int, str]] = [Ok(1), Ok(2), Ok(3)]
    collected = collect(results)

    match collected:
        case Ok(values):
            assert values == [1, 2, 3]
        case Err():
            raise AssertionError("Should be Ok")


def test_collect_with_err() -> None:
    """collect returns first Err encountered."""
    results: list[Result[int, str]] = [Ok(1), Err("bad"), Ok(3)]
    collected = collect(results)

    match collected:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "bad"


def test_collect_empty_list() -> None:
    """collect returns Ok([]) for empty input."""
    results: list[Result[int, str]] = []
    collected = collect(results)

    match collected:
        case Ok(values):
            assert values == []
        case Err():
            raise AssertionError("Should be Ok")


def test_collect_first_err() -> None:
    """collect returns the first Err, not a later one."""
    results: list[Result[int, str]] = [Ok(1), Err("first"), Err("second")]
    collected = collect(results)

    match collected:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "first"


# Hypothesis property tests
@given(st.integers(), st.text())
def test_property_map_ok_preserves_err(value: int, error: str) -> None:
    """map_ok on Err returns the same Err without calling function."""
    result: Result[int, str] = Err(error)

    def should_not_be_called(x: int) -> int:
        raise AssertionError("Function should not be called on Err")

    mapped = map_ok(result, should_not_be_called)

    match mapped:
        case Err(err):
            assert err == error
        case Ok():
            raise AssertionError("Should remain Err")


@given(st.integers())
def test_property_map_ok_transforms_ok(value: int) -> None:
    """map_ok on Ok applies the function to the value."""
    result: Result[int, str] = Ok(value)
    mapped = map_ok(result, lambda x: x + 1)

    match mapped:
        case Ok(new_value):
            assert new_value == value + 1
        case Err():
            raise AssertionError("Should remain Ok")


@given(st.integers(), st.text())
def test_property_and_then_preserves_err(value: int, error: str) -> None:
    """and_then on Err returns the same Err without calling function."""
    result: Result[int, str] = Err(error)

    def should_not_be_called(x: int) -> Result[int, str]:
        raise AssertionError("Function should not be called on Err")

    chained = and_then(result, should_not_be_called)

    match chained:
        case Err(err):
            assert err == error
        case Ok():
            raise AssertionError("Should remain Err")


@given(st.integers())
def test_property_and_then_chains_ok(value: int) -> None:
    """and_then on Ok applies function and returns its result."""
    result: Result[int, str] = Ok(value)
    chained = and_then(result, lambda x: Ok(x * 2))

    match chained:
        case Ok(new_value):
            assert new_value == value * 2
        case Err():
            raise AssertionError("Should be Ok")


@given(st.lists(st.integers()))
def test_property_collect_preserves_order(values: list[int]) -> None:
    """collect preserves the order of values."""
    results: list[Result[int, str]] = [Ok(v) for v in values]
    collected = collect(results)

    match collected:
        case Ok(collected_values):
            assert collected_values == values
        case Err():
            raise AssertionError("Should be Ok")


@given(st.lists(st.integers(), min_size=1), st.integers(min_value=0))
def test_property_collect_returns_first_err(values: list[int], err_index: int) -> None:
    """collect returns the first Err in the sequence."""
    err_index = err_index % len(values)
    results: list[Result[int, str]] = [
        Err(f"error_{i}") if i == err_index else Ok(v) for i, v in enumerate(values)
    ]

    collected = collect(results)

    match collected:
        case Err(error):
            assert error == f"error_{err_index}"
        case Ok():
            raise AssertionError("Should be Err")


def test_property_collect_empty_is_ok() -> None:
    """collect([]) returns Ok([])."""
    results: list[Result[int, str]] = []
    collected = collect(results)

    match collected:
        case Ok(values):
            assert values == []
        case Err():
            raise AssertionError("Should be Ok")
