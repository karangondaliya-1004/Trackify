from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): User's plain-text password

    Returns:
        str: Secure hashed password
    """
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored hash.

    Args:
        plain_password (str): Password provided by user
        hashed_password (str): Stored hashed password

    Returns:
        bool: True if password matches, else False
    """
    return pwd_context.verify(plain_password, hashed_password)
