# vicepython-core

Canonical Result and Option types for VicePython - small, boring, explicit, strongly typed algebraic data types for Python.

**Requirements**: Python 3.10+ (pattern matching) | No runtime dependencies

## What is this

`vicepython-core` provides Result[T, E] and Option[T] types that make success/failure and presence/absence explicit in your type signatures.

- **Result[T, E]**: Explicit success (Ok) or failure (Err)
- **Option[T]**: Explicit presence (Some) or absence (Nothing)

Both types force explicit handling through pattern matching rather than letting errors silently propagate.

## Installation

```bash
uv add vicepython-core
```

Or in `pyproject.toml`:

```toml
[project]
dependencies = ["vicepython-core>=0.1.0"]
```

## Documentation

- **[Getting started](docs/getting-started.md)** - 5-minute hands-on tutorial
- **[How-to guides](docs/how-to/)** - Solve specific problems
  - [Pattern matching best practices](docs/how-to/pattern-matching-best-practices.md) - Avoid common pitfalls
  - [Chain operations](docs/how-to/chaining.md)
  - [Convert at boundaries](docs/how-to/boundary-conversion.md)
  - [Collect multiple results](docs/how-to/collecting.md)
- **[API reference](docs/reference/api.md)** - Complete function documentation
- **[Design philosophy](docs/explanation/)** - Understanding the why
  - [Deliberate omissions](docs/explanation/omissions.md)
  - [Stability approach](docs/explanation/stability.md)

## Quick example

```python
from vicepython_core import Ok, Err, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

match divide(10, 2):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

## Why these helpers exist

vicepython-core provides two focused helpers to eliminate common boilerplate observed in real VP0/VP1 code:

### Used together: map_err and discard_ok_value

**map_err** translates error types at module boundaries, and **discard_ok_value** handles command-like operations where success matters but the value doesn't:

```python
from subprocess import CalledProcessError, run
from vicepython_core import Ok, Err, Result
from vicepython_core.result import map_err, discard_ok_value

def run_migration(db_path: str) -> Result[str, CalledProcessError]:
    """Run database migration command, returns output on success."""
    result = run(["migrate", "--db", db_path], capture_output=True, check=False)
    if result.returncode == 0:
        return Ok(result.stdout.decode())
    return Err(CalledProcessError(result.returncode, result.args))

# Before: nested match just to translate error types and discard value
def init_database(db_path: str) -> Result[None, str]:
    result = run_migration(db_path)
    match result:
        case Ok(_):
            return Ok(None)
        case Err(cmd_error):
            return Err(f"Migration failed: {cmd_error}")

# After: explicit error translation at the boundary
def init_database(db_path: str) -> Result[None, str]:
    return discard_ok_value(
        map_err(
            run_migration(db_path),
            lambda e: f"Migration failed: {e}"
        )
    )
```

### Used separately: discard_ok_value

For command-like operations where you only care about success/failure:

```python
from pathlib import Path
from vicepython_core import Ok, Err, Result
from vicepython_core.result import map_ok, discard_ok_value

def create_directory(path: Path) -> Result[Path, str]:
    """Create directory, returns Path on success."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return Ok(path)
    except OSError as e:
        return Err(str(e))

# Before: mapping to None feels indirect
result = map_ok(create_directory(Path("/tmp/data")), lambda _: None)

# After: explicit about discarding the value
result = discard_ok_value(create_directory(Path("/tmp/data")))
```

### Deliberate scope

We stopped at these two helpers. Common functions like `unwrap_or`, `is_ok`, `flatten`, and `zip` are deliberately omitted because they either hide control flow or haven't shown real usage pressure yet.

Pattern matching remains the primary way to work with Result values. See [Deliberate omissions](docs/explanation/omissions.md) for the full rationale.

## Type checking

Fully typed and compliant with PEP 561. All code passes `mypy --strict`.

**Note:** When using `mypy --strict`, add catch-all patterns to satisfy exhaustiveness checking:

```python
match result:
    case Ok(value):
        # Handle success
    case Err(error):
        # Handle error
    case _:
        raise AssertionError("Unreachable: Result must be Ok or Err")
```

See [Pattern matching best practices](docs/how-to/pattern-matching-best-practices.md) for more details.

## Development

```bash
./tools/check  # Run all checks
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

## License

MIT
