#!/usr/bin/env python
from github_bot_close_inactive_issues.rate_limit import main
import sys

if __name__ == "__main__":
    main(sys.argv[1:])
