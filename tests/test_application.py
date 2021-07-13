import os

from derp.application import Application
from derp.version_number import VersionNumber

dirname = os.path.dirname(__file__)


def test_application_failure():
    """An integration test of the application against a test file with errors."""
    target = os.path.join(dirname, "resources/test_package/test_module.py")
    version = "1.0.0"
    app = Application(target, version)
    app.run()

    assert not app.catastrophic_failure
    assert len(app.failures) == 1  # 1 file with failures
    failed_file = list(app.failures.keys())[0]
    assert failed_file.endswith("test_package/test_module.py")
    failures = app.failures[failed_file]
    # 4 failures: OlderDeprecatedClass (current version is past removal version),
    # cube (removed_in is not parseable),
    # quartic (no removal version specified),
    # and _old_display (current version is past removal version)
    assert len(failures) == 4
    assert app.exit() == 1


def test_application_success():
    """An integration test of the application against a test file with no errors."""
    target = os.path.join(dirname, "resources/test_package/subdirectory/another_test_module.py")
    version = "1.0.0"
    app = Application(target, version)
    app.run()
    assert len(app.failures) == 0
    assert app.exit() == 0


def test_version_parsing():
    """Test that version can be specified through a file."""
    target = os.path.join(dirname, "resources/test_package/test_module.py")
    version = os.path.join(dirname, "resources/test_package/__version__.py")
    app = Application(target, version)
    app.run()

    assert app.current_version == VersionNumber("1.2.3")
    assert not app.catastrophic_failure
    # Should catch the same failures as above
    assert len(app.failures) == 1

    # A file with too many snippets that look like version numbers
    version = os.path.join(dirname, "resources/test_package/many_versions.txt")
    app = Application(target, version)
    app.run()
    assert app.catastrophic_failure

    # A file with nothing that looks like a version number
    version = os.path.join(dirname, "resources/test_package/empty_version.txt")
    app = Application(target, version)
    app.run()
    assert app.catastrophic_failure


def test_file_gathering():
    """Test that python files are gathered from a directory and its subdirectories."""
    target = os.path.join(dirname, "resources/test_package")
    version = "1.0.0"
    app = Application(target, version)
    app.run()
    # It should check 3 files: test_module.py, __version__.py,
    # and subdirectory/another_test_module.py
    assert len(app.file_paths) == 3
