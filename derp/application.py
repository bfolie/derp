import os
import re
from typing import Optional, List, Dict
from derp.version_number import VersionNumber
from derp.walker import collect_deprecation_errors


class Application:
    """Abstract the application as a class.

    This class is stateful. It stores results as it runs and is meant to be exited
    after it runs, not reused.

    Parameters
    ----------
    target: str
        path to the file or directory to scan for deprecations
    version: str
        version number, either as a string or a path to a file that contains the version number
    """

    def __init__(self, target: str, version: str):
        self.target = target
        self.version = version
        self.current_version: Optional[VersionNumber] = None
        self.file_paths: Optional[List[str]] = None
        self.failures: Dict[str, List[str]] = None
        self.catastrophic_failure = False

    def _initialize_absolute_paths(self):
        """Initialize a list of all paths to inspect."""
        all_files = []
        target_path = os.path.join(os.getcwd(), self.target)
        if os.path.isfile(target_path):
            all_files = [target_path]
        elif os.path.isdir(target_path):
            for path, subdirs, files in os.walk(target_path):
                for name in files:
                    this_path = os.path.abspath(os.path.join(path, name))
                    all_files.append(this_path)
        else:
            raise ValueError(f"{self.target} must correspond to a file or directory")
        all_files = [file for file in all_files if file.endswith(".py")]
        if len(all_files) == 0:
            raise ValueError(f"No python modules found at {self.target}")
        self.file_paths = all_files

    def _initialize_version_number(self):
        """Initialize current version number either by parsing a file or a version string."""
        if os.path.isfile(self.version):
            with open(self.version) as fp:
                file_text = fp.read()
                # regex captures sequence of integers separated by periods, surrounded by quotes
                pattern = "[\'\"]((?:\\d+\\.)*\\d+)[\'\"]"
                matches = list(re.finditer(pattern, file_text))
                if len(matches) == 0:
                    raise ValueError(f"File {self.version} did not contain snippets that could "
                                     f"be parsed as version numbers")
                elif len(matches) == 1:
                    version_string = matches[0].groups()[0]
                    self.current_version = VersionNumber(version_string)
                else:
                    all_matches = [match.group() for match in matches]
                    raise ValueError(f"File {self.version} contains multiple snippets that could"
                                     f"be parsed as verison numbers: {all_matches}")
        else:
            self.current_version = VersionNumber(self.version)

    def initialize(self):
        """Set class attributes that are not passed in directly."""
        self._initialize_version_number()
        self._initialize_absolute_paths()

    def run_checks(self):
        """Run deprecation check against all files."""
        assert isinstance(self.current_version, VersionNumber)
        self.failures = dict()
        for file_path in self.file_paths:
            errors = collect_deprecation_errors(file_path, self.current_version)
            if errors is not None and len(errors) > 0:
                self.failures[file_path] = errors

    def report(self):
        """Print failures"""
        if self.failures:
            for path, errors in self.failures.items():
                print(f"{path}:")
                print('\t' + '\n\t'.join(errors))

    def _run(self):
        self.initialize()
        self.run_checks()
        self.report()

    def run(self):
        """Run the application, catching exceptions and keyboard interrupts"""
        try:
            self._run()
        except (ValueError, AssertionError) as exc:
            print(exc)
            self.catastrophic_failure = True
        except KeyboardInterrupt:
            print("Caught keyboard interrupt from user")
            self.catastrophic_failure = True

    def exit(self) -> int:
        """Return exit code, 0 for success or 1 for failure"""
        if self.catastrophic_failure or self.failures is not None:
            return 1
        else:
            return 0
