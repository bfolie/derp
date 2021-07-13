# derp
Derp (Deprecation Enforcement and Removal Planning) is a command-line tool for ensuring that deprecated code is removed from your python package in a timely manner.
Derp scans the application for deprecation flags and ensures that:

1. All deprecations have a planned removal version.
2. Deprecated objects are removed at the planned time.

## Usage

Install derp from pypi using pip: `pip install derp`.
Invoke derp from the command line, specifying the package or module to analyze and the current version of the software.
The command below will scan all modules in `src/my_app` and catch any deprecated code that is supposed to be removed by version 1.0.0.

```python
derp src/my_app 1.0.0
```

The current version can also be read from a file.
If `src/my_app/__version__.py` contains the version number, invoke the following.

```python
derp src/my_app src/my_app/__version__.py
```

Including this command as part of a CI/CD script will ensure that deprecations are done thoughtfully and that deprecated code is removed on schedule.

## Potentially Asked Questions

**Why use derp?**

Derp was inspired by the belief that a lean codebase is more pleasant to work in,
and as such deprecated code should be cleaned out as soon as is feasible.
Including derp in your CI/CD pipeline pushes developers to clean out deprecated code.

**What if I don't know when I want to remove a deprecated item?**

"Next major version bump" is a good default.

**What if I need to keep a deprecated item around longer than expected?**

Increase the planned removal version.
It's fine for deprecated code to stick around longer than expected, but it should happen intentionally, not because nobody got around to clearing it out.

**What type of deprecations does derp catch?**

Currently, derp only works with the [deprecation](https://pypi.org/project/deprecation/) library.
It catches a single `@deprecated` annotation on a class or method.

**What if I use a different deprecation tool or want to deprecate something that's neither a class nor a method?**

Tell me about your use case, and I might add it.
Alternatively, open a PR.
See "derp/deprecation.py" for a discussion of how to add more types of deprecations.

**What if I have multiple deprecation annotations on a single method?**

Don't do that.
Why are you doing that?

OK fine, if there's a legitimate reason to do this, let me know and I'll think about supporting it.

**Couldn't I use the `@fail_if_not_removed` decorator?**

Yeah, but that requires a developer to be conscientious every time they deprecate something.
You have to voluntarily point it to the version number, select a removal version, and add `@fail_if_not_removed` on all relevant tests.
It's easier to just slap `@deprecated()` with no arguments, move on, and forget about it.
Derp will chide you: "you need to select a removal version."
And when that version comes around it will poke you again: "time to remove this code."