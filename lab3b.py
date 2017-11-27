#!/usr/bin/env python3

# NAME: Dawei Huang, Nathan Smith
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

import sys
import os




if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("[Error]: Incorrect number of arguments.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("[Error]: File does not exist.", file=sys.stderr)
        sys.exit(1)

    # Block Consistency Audits
    # I-node Allocation Audits
    # Directory Consistency Audits
