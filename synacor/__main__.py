from __future__ import annotations

import logging

from synacor.parser import main


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
