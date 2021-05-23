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

Including this command as part of a CI/CD script will ensure that deprecations are done thoughtfully and removed on schedule.