import os
from typing import Optional, List, Dict
from derp.version_number import VersionNumber
from derp.walker import collect_deprecation_errors


class Application:

    def __init__(self, target: str, version: str):
        self.target = target
        self.version = version
        self.current_version: Optional[VersionNumber] = None
        self.file_paths: Optional[List[str]] = None
        self.failures: Dict[str, List[str]] = None
        self.catastrophic_failure = False

    def initialize(self):
        self.current_version = VersionNumber(self.version)
        # TODO: parse from a file that contains the version number

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

    def run_checks(self):
        assert isinstance(self.current_version, VersionNumber)
        self.failures = dict()
        for file_path in self.file_paths:
            errors = collect_deprecation_errors(file_path, self.current_version)
            if errors is not None and len(errors) > 0:
                self.failures[file_path] = errors

    def report(self):
        if self.failures:
            for path, errors in self.failures.items():
                print(f"{path}:")
                print('\t' + '\n\t'.join(errors))

    def _run(self):
        self.initialize()
        self.run_checks()
        self.report()

    def run(self):
        try:
            self._run()
        except (ValueError, AssertionError) as exc:
            print(exc)
            self.catastrophic_failure = True
        except KeyboardInterrupt:
            print("Caught keyboard interrupt from user")
            self.catastrophic_failure = True

    def exit(self):
        if self.catastrophic_failure or self.failures is not None:
            return 1
        else:
            return 0
