#!/usr/bin/env python3
"""Regex: Returning log messages"""

import re
from typing import List, Tuple, Optional
import logging
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS: Tuple[str, ...] = ("name", "email",
                               "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize fields"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in a log message."""
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]+",
                  lambda m: f"{m.group(1)}={redaction}", message)


def get_logger() -> logging.Logger:
    """Creates and configures the logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to a secure database using credentials from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection:
    """
    db_username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name: Optional[str] = os.getenv("PERSONAL_DATA_DB_NAME")

    if db_name is None:
        raise ValueError("Database name must be specified \
                         in PERSONAL_DATA_DB_NAME environment variable.")

    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main() -> None:
    """Main function to fetch users from the database and log them."""
    # Set up the logger with RedactingFormatter
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows from the users table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Log each row with filtered format
    for row in rows:
        log_message = f"name={row[0]}; email={row[1]}; phone={row[2]}; \
            ssn={row[3]}; password={row[4]}; ip={row[5]}; \
                last_login={row[6]}; user_agent={row[7]}"
        logger.info(log_message)

    # Close the database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
