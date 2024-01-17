import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password
    :plain_password: a plaintext password to be verified
    :hashed_password: a hashed password to be verified against
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """
    Create a hashed password
    :password: a plaintext password to be turned into a hashed value
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()