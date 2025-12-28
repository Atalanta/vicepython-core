# How to chain operations

Chain multiple Result-returning or Option-returning operations together so that errors or absence short-circuit automatically.

## Chain Result operations with and_then

Use `and_then` when you have a sequence of operations where each one might fail, and you want to stop at the first failure.

```python
from vicepython_core import Ok, Err, Result
from vicepython_core.result import and_then, map_ok

def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Invalid integer: {s}")

def validate_positive(n: int) -> Result[int, str]:
    return Ok(n) if n > 0 else Err(f"Not positive: {n}")

# Chain the operations
result = parse_int("42")
result = and_then(result, validate_positive)
result = map_ok(result, lambda x: x * 2)

match result:
    case Ok(value):
        print(f"Final value: {value}")  # Final value: 84
    case Err(error):
        print(f"Error: {error}")
```

If parsing fails, `validate_positive` never runs. If validation fails, the multiplication never happens.

## Transform Ok values with map_ok

Use `map_ok` when you want to transform a success value without changing error handling.

```python
from vicepython_core import Ok
from vicepython_core.result import map_ok

result = Ok(5)
doubled = map_ok(result, lambda x: x * 2)  # Ok(10)
```

`map_ok` applies the function only if the Result is Ok. If it's Err, the error passes through unchanged.

## Chain Option operations with and_then

```python
from vicepython_core import Some, Nothing, Option
from vicepython_core.option import and_then

def find_user(user_id: int) -> Option[int]:
    users = {1: 42, 2: 99}
    if user_id in users:
        return Some(users[user_id])
    return Nothing()

def find_score(user_id: int) -> Option[int]:
    scores = {42: 100, 99: 85}
    if user_id in scores:
        return Some(scores[user_id])
    return Nothing()

# Chain the lookups
result = find_user(1)
result = and_then(result, find_score)

match result:
    case Some(score):
        print(f"Score: {score}")  # Score: 100
    case Nothing():
        print("Not found")
```

If `find_user` returns Nothing, `find_score` never runs.

## Import helper functions explicitly

Helper functions live in their respective modules and must be imported:

```python
from vicepython_core.result import map_ok, and_then, collect
from vicepython_core.option import map_some, and_then, require_some
```

The `and_then` name exists in both modules. This duplication is intentional—the module path is part of the API. Import only the one you need, or use qualified imports to disambiguate:

```python
from vicepython_core import result, option

result.and_then(my_result, validate_positive)
option.and_then(my_option, find_score)
```

Both `result.and_then` and `option.and_then` follow the same semantic pattern (chain operations, short-circuit on failure/absence), so the shared name reinforces the conceptual similarity while the module namespace provides type safety.
