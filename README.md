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

## Type checking

Fully typed and compliant with PEP 561. All code passes `mypy --strict`.

## Development

```bash
./tools/check  # Run all checks
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

## License

MIT
