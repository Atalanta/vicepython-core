# Pattern matching best practices

This guide covers common pitfalls and best practices when using pattern matching with Result and Option types, especially with `mypy --strict`.

## Use combinators, not nested matches

**Most important rule:** Before writing nested match statements, use `and_then` and `map_ok` for chaining operations. Nested matches are almost always code smell.

**Bad - nested match sprawl (Pascal in a trenchcoat):**
```python
def init_system() -> Result[None, Error]:
    parent_result = ensure_parent_exists()
    match parent_result:
        case Err(error):
            return Err(error)
        case Ok(None):
            cmd_result = run_init_command()
            match cmd_result:
                case Ok(_output):
                    return Ok(None)
                case Err(error):
                    return Err(error)
```

**Good - use combinators:**
```python
from vicepython_core.result import and_then, map_ok

def init_system() -> Result[None, Error]:
    # Chain sequential operations
    return map_ok(
        and_then(
            ensure_parent_exists(),
            lambda _: run_init_command(),
        ),
        lambda _: None,  # Discard output
    )
```

See [How to chain operations](chaining.md) for more on `and_then` and `map_ok`.

**When to use match vs combinators:**
- **Use combinators** for sequential operations that might fail
- **Use match** when you need to branch on Result/Option contents (like Ok(True) vs Ok(False))
- **Never nest** matches more than one level deep

## Use specific variable names in nested matches

**Problem:** When you nest match statements and reuse variable names like `error`, mypy tracks the type from the first binding and gets confused when you try to bind a different type to the same name in a nested scope.

**Bad:**
```python
from vicepython_core import Ok, Err, Result

def init_and_start() -> Result[None, FileSystemError | CommandError]:
    match check_filesystem():
        case Err(error):  # error: FileSystemError
            return Err(error)
        case Ok(_):
            match run_command():
                case Err(error):  # mypy error: expects FileSystemError, got CommandError
                    return Err(error)
                case Ok(_):
                    return Ok(None)
```

**Good:**
```python
def init_and_start() -> Result[None, FileSystemError | CommandError]:
    match check_filesystem():
        case Err(fs_error):  # Specific name
            return Err(fs_error)
        case Ok(_):
            match run_command():
                case Err(cmd_error):  # Different specific name
                    return Err(cmd_error)
                case Ok(_):
                    return Ok(None)
```

**Rule:** Always use specific, descriptive variable names in match patterns:
- `fs_error` not `error`
- `parse_error` not `error`
- `cmd_error` not `error`
- `db_error` not `error`

This makes code more readable AND avoids mypy type inference issues.

## Extract nested matches to intermediate variables

When nesting matches, extract the Result to an intermediate variable first. This helps mypy track types correctly and makes the code more readable.

**Better:**
```python
def init_and_start() -> Result[None, FileSystemError | CommandError]:
    fs_result = check_filesystem()
    match fs_result:
        case Err(fs_error):
            return Err(fs_error)
        case Ok(_):
            cmd_result = run_command()
            match cmd_result:
                case Err(cmd_error):
                    return Err(cmd_error)
                case Ok(_):
                    return Ok(None)
                case _:
                    raise AssertionError("Unreachable: Result must be Ok or Err")
        case _:
            raise AssertionError("Unreachable: Result must be Ok or Err")
```

**Even better for complex cases - use early returns:**
```python
def init_and_start() -> Result[None, FileSystemError | CommandError]:
    fs_result = check_filesystem()
    match fs_result:
        case Err(fs_error):
            return Err(fs_error)
        case Ok(_):
            pass  # Continue
        case _:
            raise AssertionError("Unreachable: Result must be Ok or Err")

    cmd_result = run_command()
    match cmd_result:
        case Err(cmd_error):
            return Err(cmd_error)
        case Ok(_):
            return Ok(None)
        case _:
            raise AssertionError("Unreachable: Result must be Ok or Err")
```

This flattens the nesting and makes the control flow clearer.

## Always add catch-all patterns for mypy --strict

With `mypy --strict`, exhaustiveness checking requires explicit catch-all patterns even when you know all cases are covered.

**Without catch-all (mypy error):**
```python
match result:
    case Ok(value):
        return value
    case Err(error):
        return None
# mypy error: Missing return statement
```

**With catch-all (mypy passes):**
```python
match result:
    case Ok(value):
        return value
    case Err(error):
        return None
    case _:
        raise AssertionError("Unreachable: Result must be Ok or Err")
```

**Rule:** Always add `case _: raise AssertionError("Unreachable")` at the end of your match statements when using `mypy --strict`.

This serves two purposes:
1. Satisfies mypy's exhaustiveness checking
2. Documents that you've considered all cases and believe this is unreachable

## Don't check state with if statements

**Bad:**
```python
# Don't do this - defeats the purpose of Result types
result = divide(10, 2)
if isinstance(result, Ok):
    value = result.value
else:
    error = result.value
```

**Good:**
```python
# Use pattern matching - forces exhaustive handling
result = divide(10, 2)
match result:
    case Ok(value):
        # Handle success
    case Err(error):
        # Handle error
    case _:
        raise AssertionError("Unreachable")
```

Pattern matching is not just syntax sugar - it integrates with Python's type system to provide type narrowing and exhaustiveness checking.

## Stop writing nested matches - you missed the point

**If you're writing this, you're doing it wrong:**

```python
# DON'T WRITE THIS - this is Pascal/C in a Python trenchcoat
def complex_operation() -> Result[str, Error]:
    match step_one():
        case Err(error):
            return Err(error)
        case Ok(value1):
            match step_two(value1):
                case Err(error):
                    return Err(error)
                case Ok(value2):
                    match step_three(value2):
                        case Err(error):
                            return Err(error)
                        case Ok(value3):
                            return Ok(value3)
```

**This is what you should have written:**

```python
from vicepython_core.result import and_then

def complex_operation() -> Result[str, Error]:
    result = step_one()
    result = and_then(result, step_two)
    result = and_then(result, step_three)
    return result
```

The entire point of Result types is that operations compose. Use `and_then` and `map_ok` to chain them. See [How to chain operations](chaining.md).

## Summary

1. **USE COMBINATORS FIRST** - `and_then` and `map_ok` for chaining, not nested matches
2. **Use specific variable names** in match patterns (`fs_error`, `cmd_error`, not `error`)
3. **Always add catch-all patterns** with `AssertionError` for mypy --strict
4. **Prefer pattern matching** over isinstance checks
5. **Never nest matches** more than one level deep - if you need to, you missed the combinators
