#!/usr/bin/env python3
"""Regex: Returning log messages"""

import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscates specified fields in a log message."""
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]+",
                  lambda m: f"{m.group(1)}={redaction}", message)
