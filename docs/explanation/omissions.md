# Deliberate omissions

This document explains features commonly found in Result/Option libraries that vicepython-core deliberately omits.

The library pushes users toward explicit error handling by omitting convenience methods that enable sloppy practices.

## unwrap_or

**What it is:** A method that returns the Ok/Some value, or a default if Err/Nothing.

```python
# Not included
value = result.unwrap_or(42)
```

**Why omitted:** While legitimate in some cases, `unwrap_or` papers over domain thinking. It makes defaulting too easy, encouraging users to avoid explicit decisions about what the default should mean.

**Use instead:** Pattern matching makes the default decision explicit at the point of use:

```python
match result:
    case Ok(value):
        use(value)
    case Err(_):
        use(42)  # Explicit choice, clear intent
```

## is_ok / is_err predicates

**What they are:** Boolean methods to check Result state without pattern matching.

```python
# Not included
if result.is_ok():
    value = result.unwrap()  # Dangerous
```

**Why omitted:** Predicates encourage "check then forget to handle" style. You check the state, then forget to handle the error case, or worse, call `.unwrap()` assuming safety.

**Use instead:** Pattern matching forces exhaustive handling of both cases at the point of use:

```python
match result:
    case Ok(value):
        # Handle success
    case Err(error):
        # Handle failure - can't forget this
```

## map_err

**What it is:** Transform the error type while leaving Ok unchanged.

```python
# Not included
result.map_err(lambda e: f"Error: {e}")
```

**Why omitted:** Useful but less common early on. It tends to appear when you have layered modules and want to normalize errors at seams between modules.

**Philosophy:** Add it when that pain shows up in real use, not preemptively. The library remains minimal until concrete need emerges.

## collect_all_errors

**What it is:** Collect multiple Results, gathering all errors instead of failing fast.

```python
# Not included
collected = collect_all_errors(results)  # Would return Ok or Err with list of errors
```

**Why omitted:** Valuable mainly for validation UX (forms, config validation, batch imports), but requires designing an "error collection" type and presentation strategy.

This is a real commitment requiring domain-specific error types. It should emerge from concrete validation needs, not be added speculatively.

**Use instead:** The `collect` function implements fail-fast semantics, which covers most cases. When you need to gather all errors, design your error collection strategy first, then build it specifically for your domain.

## Exception → Result helpers

**What they are:** Generic wrappers to convert any exception into Result.

```python
# Not included
result = catch_exceptions(lambda: risky_operation())
```

**Why omitted:** Exception-to-Result conversions are inherently boundary-specific. A generic wrapper would either:
- Bake in specific Exception types (too narrow)
- Encourage blanket catching (too broad, hides bugs)

**Philosophy:** If needed, these belong in a separate boundary-specific package with explicit wrappers per boundary (subprocess, requests, yaml/json parsing). Don't include generic exception catching in a core types library.

**Use instead:** Wrap exceptions explicitly at boundaries:

```python
def parse_config(path: str) -> Result[Config, str]:
    try:
        return Ok(yaml.safe_load(open(path)))
    except FileNotFoundError:
        return Err(f"Config file not found: {path}")
    except yaml.YAMLError as e:
        return Err(f"Invalid YAML: {e}")
```

Explicit error handling at boundaries makes error cases visible and typed.

## Type guards

**What they are:** Functions that narrow types without pattern matching.

```python
# Not included
if is_ok(result):
    value = result.value  # Type narrowed to Ok
```

**Why omitted:** Pattern matching is sufficient for type narrowing in Python 3.10+. Type guards reintroduce the "boolean check then proceed" habit that vicepython avoids.

**Use instead:** Pattern matching provides type narrowing automatically:

```python
match result:
    case Ok(value):
        # value is automatically narrowed to T
        use(value)
```

## Philosophy

Keep the library small and opinionated toward explicit handling. If you need these features, the domain will make it obvious, and you can add them then.

Don't add features preemptively. Wait for real pain, then solve it deliberately.
