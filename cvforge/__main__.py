"""Allow ``python -m cvforge``."""

import sys

from .cli import main

sys.exit(main())
