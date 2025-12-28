"""Integration smoke tests showing realistic usage patterns.

Tests demonstrate how to combine helpers in chains and realistic scenarios.
"""

from vicepython_core import Err, Nothing, Ok, Option, Result
from vicepython_core.option import option_from_optional, require_some
from vicepython_core.result import and_then, collect, map_ok


def test_chaining_result_operations() -> None:
    """Multiple Result operations can be chained together."""

    def parse_int(s: str) -> Result[int, str]:
        try:
            return Ok(int(s))
        except ValueError:
            return Err(f"Invalid integer: {s}")

    def validate_positive(n: int) -> Result[int, str]:
        if n > 0:
            return Ok(n)
        return Err(f"Not positive: {n}")

    def double(n: int) -> Result[int, str]:
        return Ok(n * 2)

    # Success path
    result = parse_int("42")
    result = and_then(result, validate_positive)
    result = and_then(result, double)

    match result:
        case Ok(value):
            assert value == 84
        case Err():
            raise AssertionError("Should succeed")

    # Failure path - invalid integer
    result = parse_int("not a number")
    result = and_then(result, validate_positive)
    result = and_then(result, double)

    match result:
        case Err(error):
            assert "Invalid integer" in error
        case Ok():
            raise AssertionError("Should fail")

    # Failure path - not positive
    result = parse_int("-5")
    result = and_then(result, validate_positive)
    result = and_then(result, double)

    match result:
        case Err(error):
            assert "Not positive" in error
        case Ok():
            raise AssertionError("Should fail")


def test_collecting_multiple_results() -> None:
    """collect can gather results from multiple operations."""

    def parse_int(s: str) -> Result[int, str]:
        try:
            return Ok(int(s))
        except ValueError:
            return Err(f"Invalid integer: {s}")

    # All succeed
    inputs = ["1", "2", "3", "4", "5"]
    results = [parse_int(s) for s in inputs]
    collected = collect(results)

    match collected:
        case Ok(values):
            assert values == [1, 2, 3, 4, 5]
        case Err():
            raise AssertionError("Should succeed")

    # One fails
    inputs = ["1", "2", "bad", "4", "5"]
    results = [parse_int(s) for s in inputs]
    collected = collect(results)

    match collected:
        case Err(error):
            assert "bad" in error
        case Ok():
            raise AssertionError("Should fail")


def test_option_to_result_conversion() -> None:
    """Options can be converted to Results with custom errors."""

    def lookup_config(key: str) -> Option[str]:
        config = {"host": "localhost", "port": "8080"}
        value = config.get(key)
        return option_from_optional(value)

    # Present key
    opt = lookup_config("host")
    result = require_some(opt, "Missing config key: host")

    match result:
        case Ok(value):
            assert value == "localhost"
        case Err():
            raise AssertionError("Should succeed")

    # Missing key
    opt = lookup_config("database")
    result = require_some(opt, "Missing config key: database")

    match result:
        case Err(error):
            assert error == "Missing config key: database"
        case Ok():
            raise AssertionError("Should fail")


def test_combining_option_and_result() -> None:
    """Options and Results can be combined in realistic workflows."""

    def get_user_id(username: str | None) -> Option[int]:
        users = {"alice": 1, "bob": 2}
        if username is None:
            return Nothing()
        user_id = users.get(username)
        return option_from_optional(user_id)

    def fetch_user_data(user_id: int) -> Result[dict[str, str], str]:
        data = {1: {"name": "Alice", "email": "alice@example.com"}, 2: {"name": "Bob"}}
        if user_id in data:
            return Ok(data[user_id])
        return Err(f"User {user_id} not found")

    def get_email(user_data: dict[str, str]) -> Result[str, str]:
        email = user_data.get("email")
        if email is not None:
            return Ok(email)
        return Err("Email not found in user data")

    # Success path
    user_id_opt = get_user_id("alice")
    result = require_some(user_id_opt, "Username not found")
    result = and_then(result, fetch_user_data)
    result = and_then(result, get_email)

    match result:
        case Ok(email):
            assert email == "alice@example.com"
        case Err():
            raise AssertionError("Should succeed")

    # Failure - no username
    user_id_opt = get_user_id(None)
    result = require_some(user_id_opt, "Username not found")
    result = and_then(result, fetch_user_data)
    result = and_then(result, get_email)

    match result:
        case Err(error):
            assert error == "Username not found"
        case Ok():
            raise AssertionError("Should fail")

    # Failure - user exists but no email
    user_id_opt = get_user_id("bob")
    result = require_some(user_id_opt, "Username not found")
    result = and_then(result, fetch_user_data)
    result = and_then(result, get_email)

    match result:
        case Err(error):
            assert error == "Email not found in user data"
        case Ok():
            raise AssertionError("Should fail")


def test_map_ok_in_pipeline() -> None:
    """map_ok can be used to transform values in a pipeline."""

    def parse_int(s: str) -> Result[int, str]:
        try:
            return Ok(int(s))
        except ValueError:
            return Err(f"Invalid integer: {s}")

    # Transform with map_ok
    result = parse_int("21")
    result = map_ok(result, lambda x: x * 2)
    result = map_ok(result, lambda x: x + 10)

    match result:
        case Ok(value):
            assert value == 52  # (21 * 2) + 10
        case Err():
            raise AssertionError("Should succeed")

    # Error propagates through map_ok chain
    result = parse_int("not a number")
    result = map_ok(result, lambda x: x * 2)
    result = map_ok(result, lambda x: x + 10)

    match result:
        case Err(error):
            assert "Invalid integer" in error
        case Ok():
            raise AssertionError("Should fail")


def test_collect_then_transform() -> None:
    """collect can be combined with other operations."""
    results = [Ok(1), Ok(2), Ok(3)]
    collected = collect(results)

    # Transform collected list
    final = map_ok(collected, lambda values: sum(values))

    match final:
        case Ok(total):
            assert total == 6
        case Err():
            raise AssertionError("Should succeed")
