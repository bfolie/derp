import argparse
import sys
from typing import Optional, List
from .application import Application


__name__ = "derp"


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog='derp')
    parser.add_argument("target")
    parser.add_argument("version")
    args = parser.parse_args(argv)

    app = Application(target=args.target, version=args.version)
    app.run()
    return app.exit()


if __name__ == '__main__':
    sys.exit(main())
