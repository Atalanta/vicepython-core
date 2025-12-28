# How to convert at boundaries

Convert external representations (Optional, exceptions) into Result or Option at the point where your code receives data from outside libraries.

## Convert Optional[T] to Option[T]

Use `option_from_optional` when external libraries return `T | None`:

```python
from vicepython_core import Option
from vicepython_core.option import option_from_optional

def get_config_value(key: str) -> Option[str]:
    config = {"host": "localhost", "port": "8080"}
    value = config.get(key)  # Returns Optional[str]
    return option_from_optional(value)
```

This makes the optional value explicit in your function signature.

## Convert Option[T] to Result[T, E]

Use `require_some` when you need to treat Nothing as an error:

```python
from vicepython_core import Some, Nothing, Result
from vicepython_core.option import require_some

opt = Some(42)
result = require_some(opt, "Value missing")  # Ok(42)

opt = Nothing()
result = require_some(opt, "Value missing")  # Err("Value missing")
```

This is useful when optional values are valid internally, but missing values are errors at specific boundaries.

## Convert exceptions to Result

Wrap exception-raising code in try/except at boundaries. This conversion is intentionally handwritten at each boundary rather than using a generic helper:

```python
from vicepython_core import Ok, Err, Result

def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Invalid integer: {s}")
```

Catch specific exceptions and convert them to typed errors. Avoid catching bare `Exception` unless you have a specific reason.

The library deliberately provides no generic exception-to-Result helper because conversions are boundary-specific. Each boundary has different exception types and error semantics, so the conversion logic should be explicit at each call site.

## When to convert

Convert at **system boundaries** where your code interfaces with:
- External libraries
- User input
- Network responses
- File I/O
- Database queries

Keep Result and Option throughout your internal code. Only convert at the edges.

## What not to do

Don't convert back and forth within your code:

```python
# Bad: Converting back and forth
def process(value: Option[int]) -> int:
    match value:
        case Some(n):
            return n
        case Nothing():
            return 0

# Better: Keep Option and handle at the boundary
def process(value: Option[int]) -> Option[int]:
    return map_some(value, lambda x: x * 2)
```

Let Result and Option flow through your code naturally. Handle them at the final boundary where you produce output.
