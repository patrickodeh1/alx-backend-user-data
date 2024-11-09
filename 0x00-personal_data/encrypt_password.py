#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt, using a salt."""
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password
