# Getting started

This tutorial walks you through using vicepython-core's Result and Option types for the first time.

You'll learn by doing: writing functions that handle errors explicitly with Result, and optional values explicitly with Option.

## Prerequisites

- Python 3.10 or later (for pattern matching syntax)
- A Python project with vicepython-core installed

If you haven't installed it yet, run:

```bash
uv add vicepython-core
```

## Your first Result

Result represents operations that can succeed or fail. Instead of raising exceptions or returning None, you return `Ok(value)` for success or `Err(error)` for failure.

Create a new file `example.py`:

```python
from vicepython_core import Ok, Err, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)
```

Notice the return type `Result[float, str]`:
- `float` is the success type (what you get in Ok)
- `str` is the error type (what you get in Err)

Now use pattern matching to handle both cases:

```python
result = divide(10, 2)
match result:
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

Run your file:

```bash
python example.py
```

You should see: `Result: 5.0`

Change the code to `divide(10, 0)` and run again. You'll see: `Error: Division by zero`

## Your first Option

Option represents values that might be absent. Instead of returning None, you return `Some(value)` when present or `Nothing()` when absent.

Add this to `example.py`:

```python
from vicepython_core import Some, Nothing, Option

def find_user(user_id: int) -> Option[str]:
    users = {1: "Alice", 2: "Bob"}
    if user_id in users:
        return Some(users[user_id])
    return Nothing()
```

The return type `Option[str]` means:
- `str` is what you get in Some
- Nothing carries no value

Handle both cases with pattern matching:

```python
user = find_user(1)
match user:
    case Some(name):
        print(f"Found user: {name}")
    case Nothing():
        print("User not found")
```

Try `find_user(1)` (prints "Found user: Alice") and `find_user(99)` (prints "User not found").

## Converting at boundaries

When working with external libraries that return `Optional[T]` or raise exceptions, convert to Result or Option at the boundary.

### Converting Optional to Option

```python
from vicepython_core.option import option_from_optional

def get_config_value(key: str) -> Option[str]:
    config = {"host": "localhost", "port": "8080"}
    value = config.get(key)  # Returns Optional[str]
    return option_from_optional(value)
```

### Converting exceptions to Result

```python
def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Invalid integer: {s}")
```

Wrap the exception-raising code in try/except and convert to Result at the boundary.

## Next steps

You now know:
- How to create Result and Option values
- How to handle them with pattern matching
- How to convert from Optional and exceptions

**Important:** Before writing complex code, read [Pattern matching best practices](how-to/pattern-matching-best-practices.md) to avoid common pitfalls with nested matches and mypy --strict.

Continue to the other how-to guides to learn specific tasks like chaining operations and collecting multiple results.
