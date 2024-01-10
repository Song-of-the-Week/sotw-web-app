from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password
    :plain_password: a plaintext password to be verified
    :hashed_password: a hashed password to be verified against
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Create a hashed password
    :password: a plaintext password to be turned into a hashed value
    """
    return PWD_CONTEXT.hash(password)