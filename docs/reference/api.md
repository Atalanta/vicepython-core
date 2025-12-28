# API reference

Complete reference for all types and functions in vicepython-core.

## Core types

### Result[T, E]

Represents explicit success (Ok) or failure (Err).

```python
from vicepython_core import Result, Ok, Err
```

**Type parameters:**
- `T`: Success value type
- `E`: Error value type

**Constructors:**

#### Ok(value: T) -> Result[T, E]

Creates a successful Result containing `value`.

```python
result = Ok(42)  # Result[int, str]
```

#### Err(error: E) -> Result[T, E]

Creates a failed Result containing `error`.

```python
result = Err("Something went wrong")  # Result[int, str]
```

**Pattern matching:**

```python
match result:
    case Ok(value):
        # value has type T
        ...
    case Err(error):
        # error has type E
        ...
```

### Option[T]

Represents explicit presence (Some) or absence (Nothing).

```python
from vicepython_core import Option, Some, Nothing
```

**Type parameters:**
- `T`: Value type when present

**Constructors:**

#### Some(value: T) -> Option[T]

Creates an Option containing `value`.

```python
opt = Some(42)  # Option[int]
```

#### Nothing() -> Option[T]

Creates an empty Option.

```python
opt = Nothing()  # Option[int]
```

**Pattern matching:**

```python
match opt:
    case Some(value):
        # value has type T
        ...
    case Nothing():
        # no value
        ...
```

## Result helpers

Import from `vicepython_core.result`:

```python
from vicepython_core.result import map_ok, and_then, collect
```

### map_ok(result: Result[T, E], f: Callable[[T], U]) -> Result[U, E]

Applies function `f` to the value inside Ok. Returns the original Err unchanged.

**Parameters:**
- `result`: The Result to transform
- `f`: Function to apply to Ok value

**Returns:**
- `Ok(f(value))` if result is `Ok(value)`
- Original `Err(error)` if result is `Err(error)`

**Example:**

```python
result = Ok(5)
doubled = map_ok(result, lambda x: x * 2)  # Ok(10)

result = Err("bad")
doubled = map_ok(result, lambda x: x * 2)  # Err("bad")
```

### and_then(result: Result[T, E], f: Callable[[T], Result[U, E]]) -> Result[U, E]

Chains a Result-returning function. Short-circuits on Err.

**Parameters:**
- `result`: The Result to chain from
- `f`: Function that takes T and returns Result[U, E]

**Returns:**
- `f(value)` if result is `Ok(value)`
- Original `Err(error)` if result is `Err(error)`

**Example:**

```python
def validate_positive(n: int) -> Result[int, str]:
    return Ok(n) if n > 0 else Err("Not positive")

result = Ok(42)
validated = and_then(result, validate_positive)  # Ok(42)

result = Ok(-5)
validated = and_then(result, validate_positive)  # Err("Not positive")
```

### collect(results: Sequence[Result[T, E]]) -> Result[list[T], E]

Combines multiple Results into a single Result. Fails fast on first Err.

**Parameters:**
- `results`: Sequence of Results to collect

**Returns:**
- `Ok(list of all values)` if all Results are Ok
- First `Err` encountered, or `Ok([])` for empty input

**Example:**

```python
results = [Ok(1), Ok(2), Ok(3)]
collected = collect(results)  # Ok([1, 2, 3])

results = [Ok(1), Err("bad"), Ok(3)]
collected = collect(results)  # Err("bad")

collected = collect([])  # Ok([])
```

## Option helpers

Import from `vicepython_core.option`:

```python
from vicepython_core.option import map_some, and_then, option_from_optional, require_some
```

### map_some(opt: Option[T], f: Callable[[T], U]) -> Option[U]

Applies function `f` to the value inside Some. Returns Nothing unchanged.

**Parameters:**
- `opt`: The Option to transform
- `f`: Function to apply to Some value

**Returns:**
- `Some(f(value))` if opt is `Some(value)`
- `Nothing()` if opt is `Nothing()`

**Example:**

```python
opt = Some(5)
doubled = map_some(opt, lambda x: x * 2)  # Some(10)

opt = Nothing()
doubled = map_some(opt, lambda x: x * 2)  # Nothing()
```

### and_then(opt: Option[T], f: Callable[[T], Option[U]]) -> Option[U]

Chains an Option-returning function. Short-circuits on Nothing.

**Parameters:**
- `opt`: The Option to chain from
- `f`: Function that takes T and returns Option[U]

**Returns:**
- `f(value)` if opt is `Some(value)`
- `Nothing()` if opt is `Nothing()`

**Example:**

```python
def find_score(user_id: int) -> Option[int]:
    scores = {42: 100, 99: 85}
    if user_id in scores:
        return Some(scores[user_id])
    return Nothing()

opt = Some(42)
score = and_then(opt, find_score)  # Some(100)

opt = Nothing()
score = and_then(opt, find_score)  # Nothing()
```

### option_from_optional(value: T | None) -> Option[T]

Converts Python Optional (T | None) to Option[T].

**Parameters:**
- `value`: Optional value to convert

**Returns:**
- `Some(value)` if value is not None
- `Nothing()` if value is None

**Example:**

```python
config = {"host": "localhost"}
value = config.get("host")  # Optional[str]
opt = option_from_optional(value)  # Some("localhost")

value = config.get("missing")  # None
opt = option_from_optional(value)  # Nothing()
```

### require_some(opt: Option[T], error: E) -> Result[T, E]

Converts Option to Result, providing error for Nothing case.

**Parameters:**
- `opt`: The Option to convert
- `error`: Error value to use if opt is Nothing

**Returns:**
- `Ok(value)` if opt is `Some(value)`
- `Err(error)` if opt is `Nothing()`

**Example:**

```python
opt = Some(42)
result = require_some(opt, "Value missing")  # Ok(42)

opt = Nothing()
result = require_some(opt, "Value missing")  # Err("Value missing")
```
