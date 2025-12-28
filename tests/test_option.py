"""Tests for Option helper functions.

Example tests and hypothesis property tests focusing on practical invariants.
"""

from hypothesis import given
from hypothesis import strategies as st

from vicepython_core import Err, Nothing, Ok, Option, Some
from vicepython_core.option import and_then, map_some, option_from_optional, require_some


# Example tests for map_some
def test_map_some_with_some() -> None:
    """map_some applies function to Some value."""
    opt: Option[int] = Some(5)
    mapped = map_some(opt, lambda x: x * 2)

    match mapped:
        case Some(value):
            assert value == 10
        case Nothing():
            raise AssertionError("Should be Some")


def test_map_some_with_nothing() -> None:
    """map_some leaves Nothing unchanged."""
    opt: Option[int] = Nothing()
    mapped = map_some(opt, lambda x: x * 2)

    match mapped:
        case Some():
            raise AssertionError("Should be Nothing")
        case Nothing():
            assert True


# Example tests for and_then
def test_and_then_with_some() -> None:
    """and_then chains Some value through function."""
    opt: Option[int] = Some(5)
    chained = and_then(opt, lambda x: Some(x * 2))

    match chained:
        case Some(value):
            assert value == 10
        case Nothing():
            raise AssertionError("Should be Some")


def test_and_then_with_some_returning_nothing() -> None:
    """and_then can convert Some to Nothing."""
    opt: Option[int] = Some(5)
    chained = and_then(opt, lambda x: Nothing())

    match chained:
        case Some():
            raise AssertionError("Should be Nothing")
        case Nothing():
            assert True


def test_and_then_with_nothing() -> None:
    """and_then leaves Nothing unchanged."""
    opt: Option[int] = Nothing()
    chained = and_then(opt, lambda x: Some(x * 2))

    match chained:
        case Some():
            raise AssertionError("Should be Nothing")
        case Nothing():
            assert True


# Example tests for option_from_optional
def test_option_from_optional_with_value() -> None:
    """option_from_optional converts non-None to Some."""
    opt = option_from_optional(42)

    match opt:
        case Some(value):
            assert value == 42
        case Nothing():
            raise AssertionError("Should be Some")


def test_option_from_optional_with_none() -> None:
    """option_from_optional converts None to Nothing."""
    opt = option_from_optional(None)

    match opt:
        case Some():
            raise AssertionError("Should be Nothing")
        case Nothing():
            assert True


# Example tests for require_some
def test_require_some_with_some() -> None:
    """require_some converts Some to Ok."""
    opt: Option[int] = Some(42)
    result = require_some(opt, "missing value")

    match result:
        case Ok(value):
            assert value == 42
        case Err():
            raise AssertionError("Should be Ok")


def test_require_some_with_nothing() -> None:
    """require_some converts Nothing to Err with provided error."""
    opt: Option[int] = Nothing()
    result = require_some(opt, "missing value")

    match result:
        case Ok():
            raise AssertionError("Should be Err")
        case Err(error):
            assert error == "missing value"


# Hypothesis property tests
@given(st.integers())
def test_property_map_some_preserves_nothing(value: int) -> None:
    """map_some on Nothing returns Nothing without calling function."""
    opt: Option[int] = Nothing()

    def should_not_be_called(x: int) -> int:
        raise AssertionError("Function should not be called on Nothing")

    mapped = map_some(opt, should_not_be_called)

    match mapped:
        case Nothing():
            assert True
        case Some():
            raise AssertionError("Should remain Nothing")


@given(st.integers())
def test_property_map_some_transforms_some(value: int) -> None:
    """map_some on Some applies the function to the value."""
    opt: Option[int] = Some(value)
    mapped = map_some(opt, lambda x: x + 1)

    match mapped:
        case Some(new_value):
            assert new_value == value + 1
        case Nothing():
            raise AssertionError("Should remain Some")


@given(st.integers())
def test_property_and_then_preserves_nothing(value: int) -> None:
    """and_then on Nothing returns Nothing without calling function."""
    opt: Option[int] = Nothing()

    def should_not_be_called(x: int) -> Option[int]:
        raise AssertionError("Function should not be called on Nothing")

    chained = and_then(opt, should_not_be_called)

    match chained:
        case Nothing():
            assert True
        case Some():
            raise AssertionError("Should remain Nothing")


@given(st.integers())
def test_property_and_then_chains_some(value: int) -> None:
    """and_then on Some applies function and returns its result."""
    opt: Option[int] = Some(value)
    chained = and_then(opt, lambda x: Some(x * 2))

    match chained:
        case Some(new_value):
            assert new_value == value * 2
        case Nothing():
            raise AssertionError("Should be Some")


@given(st.integers())
def test_property_option_from_optional_some(value: int) -> None:
    """option_from_optional converts non-None to Some with same value."""
    opt = option_from_optional(value)

    match opt:
        case Some(v):
            assert v == value
        case Nothing():
            raise AssertionError("Should be Some")


def test_property_option_from_optional_none() -> None:
    """option_from_optional converts None to Nothing."""
    opt = option_from_optional(None)

    match opt:
        case Nothing():
            assert True
        case Some():
            raise AssertionError("Should be Nothing")


@given(st.integers(), st.text())
def test_property_require_some_ok(value: int, error_message: str) -> None:
    """require_some on Some returns Ok with same value."""
    opt: Option[int] = Some(value)
    result = require_some(opt, error_message)

    match result:
        case Ok(v):
            assert v == value
        case Err():
            raise AssertionError("Should be Ok")


@given(st.text())
def test_property_require_some_err(error_message: str) -> None:
    """require_some on Nothing returns Err with provided error."""
    opt: Option[int] = Nothing()
    result = require_some(opt, error_message)

    match result:
        case Err(err):
            assert err == error_message
        case Ok():
            raise AssertionError("Should be Err")
