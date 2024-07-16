import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password

    Args:
        plain_password (str): A plaintext password to be verified.
        hashed_password (str): A hashed password to be verified against.

    Returns:
        bool: True if the password is authenticated and False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """
    Create a hashed password

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: A hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()
