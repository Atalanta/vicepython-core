"""Tests for core type definitions.

Basic instantiation, pattern matching, and type assertions for Result and Option.
"""

from vicepython_core import Err, Nothing, Ok, Option, Result, Some


def test_ok_instantiation() -> None:
    """Ok can be instantiated with a value."""
    result: Result[int, str] = Ok(42)
    assert result.value == 42
    assert result.kind == "ok"


def test_err_instantiation() -> None:
    """Err can be instantiated with an error."""
    result: Result[int, str] = Err("something went wrong")
    assert result.error == "something went wrong"
    assert result.kind == "err"


def test_some_instantiation() -> None:
    """Some can be instantiated with a value."""
    opt: Option[int] = Some(42)
    assert opt.value == 42
    assert opt.kind == "some"


def test_nothing_instantiation() -> None:
    """Nothing can be instantiated."""
    opt: Option[int] = Nothing()
    assert opt.kind == "nothing"


def test_result_pattern_matching_ok() -> None:
    """Pattern matching works correctly for Ok."""
    result: Result[int, str] = Ok(42)

    match result:
        case Ok(value):
            assert value == 42
        case Err():
            raise AssertionError("Should not match Err")


def test_result_pattern_matching_err() -> None:
    """Pattern matching works correctly for Err."""
    result: Result[int, str] = Err("error")

    match result:
        case Ok():
            raise AssertionError("Should not match Ok")
        case Err(error):
            assert error == "error"


def test_option_pattern_matching_some() -> None:
    """Pattern matching works correctly for Some."""
    opt: Option[int] = Some(42)

    match opt:
        case Some(value):
            assert value == 42
        case Nothing():
            raise AssertionError("Should not match Nothing")


def test_option_pattern_matching_nothing() -> None:
    """Pattern matching works correctly for Nothing."""
    opt: Option[int] = Nothing()

    match opt:
        case Some():
            raise AssertionError("Should not match Some")
        case Nothing():
            assert True


def test_result_with_different_types() -> None:
    """Result can hold different value and error types."""
    result_int: Result[int, str] = Ok(42)
    result_str: Result[str, Exception] = Err(ValueError("bad"))

    assert isinstance(result_int, Ok)
    assert isinstance(result_str, Err)


def test_option_with_different_types() -> None:
    """Option can hold different value types."""
    opt_int: Option[int] = Some(42)
    opt_str: Option[str] = Some("hello")
    opt_nothing: Option[float] = Nothing()

    assert isinstance(opt_int, Some)
    assert isinstance(opt_str, Some)
    assert isinstance(opt_nothing, Nothing)


def test_frozen_ok() -> None:
    """Ok instances are frozen (immutable)."""
    result = Ok(42)
    try:
        result.value = 100  # type: ignore[misc]
        raise AssertionError("Should not be able to modify frozen dataclass")
    except AttributeError:
        pass


def test_frozen_err() -> None:
    """Err instances are frozen (immutable)."""
    result = Err("error")
    try:
        result.error = "new error"  # type: ignore[misc]
        raise AssertionError("Should not be able to modify frozen dataclass")
    except AttributeError:
        pass


def test_frozen_some() -> None:
    """Some instances are frozen (immutable)."""
    opt = Some(42)
    try:
        opt.value = 100  # type: ignore[misc]
        raise AssertionError("Should not be able to modify frozen dataclass")
    except AttributeError:
        pass


def test_frozen_nothing() -> None:
    """Nothing instances are frozen (immutable)."""
    opt = Nothing()
    try:
        opt.kind = "something"  # type: ignore[misc]
        raise AssertionError("Should not be able to modify frozen dataclass")
    except AttributeError:
        pass
