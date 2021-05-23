import argparse
import sys
from typing import Optional, List
from derp.application import Application


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog='derp')
    parser.add_argument("target", help="file or directory to scan for deprecations")
    version_help = "current version of your software, either passed as a string or a path to a " \
                   "file that contains the version. Must be specified as a sequence of integers " \
                   "separated by periods, e.g., '1.23.4'."
    parser.add_argument("version", help=version_help)
    args = parser.parse_args(argv)

    app = Application(target=args.target, version=args.version)
    app.run()
    return app.exit()


if __name__ == '__main__':
    sys.exit(main())
