# How to collect multiple results

Combine multiple Result values into a single Result that succeeds only if all inputs succeed.

## Collect a list of Results

Use `collect` when you have multiple operations that might fail, and you want either all successes or the first failure:

```python
from vicepython_core import Ok, Err, Result
from vicepython_core.result import collect

def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Invalid integer: {s}")

# Parse multiple strings
results = [parse_int("1"), parse_int("2"), parse_int("3")]
collected = collect(results)

match collected:
    case Ok(values):
        print(f"All parsed: {values}")  # All parsed: [1, 2, 3]
    case Err(error):
        print(f"First error: {error}")
```

If any input is Err, `collect` returns that Err immediately (fail-fast). If all inputs are Ok, it returns Ok with a list of all the values.

## Fail-fast behavior

`collect` stops at the first error:

```python
results = [Ok(1), Err("bad"), Ok(3), Err("worse")]
collected = collect(results)  # Err("bad")
```

The third and fourth items are never examined. This is intentional: `collect` implements fail-fast semantics.

## Empty input

An empty list is treated as success:

```python
from vicepython_core.result import collect

collected = collect([])  # Ok([])
```

This is consistent with the idea that "no failures occurred."

## Use with map

Combine `collect` with list comprehensions or map to process multiple items:

```python
from vicepython_core.result import collect

def validate_positive(n: int) -> Result[int, str]:
    return Ok(n) if n > 0 else Err(f"Not positive: {n}")

numbers = [1, 2, 3, 4, 5]
results = [validate_positive(n) for n in numbers]
collected = collect(results)

match collected:
    case Ok(values):
        print(f"All valid: {values}")
    case Err(error):
        print(f"Validation failed: {error}")
```

## When not to use collect

If you need to gather **all** errors (not just the first), `collect` is not appropriate. It implements fail-fast semantics only.

For validation use cases where you want to show users all errors at once (like form validation), you need a different approach. That pattern is deliberately omitted from this library because it requires designing error collection and presentation strategies specific to your domain.
