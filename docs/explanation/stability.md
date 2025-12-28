# Stability philosophy

This document explains vicepython-core's approach to API stability and evolution.

## types.py is the stability anchor

The core types (Result, Option, Ok, Err, Some, Nothing) are the stability anchor of this library. Changes to these types are extremely rare and treated as semver-breaking even during 0.x versions.

The library culturally behaves as if 1.0 already exists. No casual evolution of core types.

## Why this matters

Result and Option are foundational abstractions. Code using these types spreads throughout a codebase quickly. Any breaking change creates cascading updates across many files.

By treating the core types as stable from the start, users can adopt vicepython-core confidently even at 0.x versions.

## Helper functions evolve carefully

Helper functions (`map_ok`, `and_then`, `collect`, etc.) are added cautiously with strong justification.

**Criteria for adding helpers:**
1. The pattern appears repeatedly in real usage
2. The helper eliminates meaningful boilerplate
3. The implementation is obvious and unlikely to need changes
4. The function name and signature are clear and intuitive

If a helper doesn't meet these criteria, it stays out of the library until real usage proves the need.

## What stability means in practice

**Stable (won't change):**
- Core type definitions (Result[T, E], Option[T])
- Constructor signatures (Ok, Err, Some, Nothing)
- Pattern matching interface

**Can evolve (with justification):**
- Helper function additions (new helpers added when patterns emerge)
- Helper function signatures (only if original design was flawed)
- Type annotations (refinements for better type checking)

**Changes require:**
- Clear justification rooted in real usage
- Discussion of migration impact
- Semver-compliant versioning

## Version semantics

Even during 0.x:
- Breaking changes to core types → 0.x to 0.(x+1)
- New helper functions → 0.x.y to 0.x.(y+1)
- Bug fixes → 0.x.y to 0.x.y.1

The library respects semantic versioning strictly, even before 1.0.

## Why keep it boring

Stability enables trust. If the library changes frequently, users can't build on it confidently.

By keeping the library boring and stable:
- Users adopt it without fear of churn
- Code reviews focus on domain logic, not library changes
- Upgrades are safe and uneventful

The library should disappear into the background. It solves the Result/Option problem once, then gets out of the way.

## When to evolve

Evolution happens when:
1. Real usage reveals a missing helper that's obviously needed
2. A type annotation improvement eliminates a class of bugs
3. A bug in existing behavior is discovered

Evolution does not happen because:
- Another library has a feature
- A feature "might be useful someday"
- Aesthetic preferences change

Wait for real pain. Solve it deliberately. Stay boring.
