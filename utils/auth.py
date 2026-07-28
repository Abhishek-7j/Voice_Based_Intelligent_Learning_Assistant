import werkzeug.security

def hash_password(password):
    """
    Hashes a plain text password using Werkzeug's secure pbkdf2:sha256 algorithm.
    """
    return werkzeug.security.generate_password_hash(password)

def verify_password(password, hashed_password):
    """
    Verifies a plain text password against a stored Werkzeug password hash.
    """
    if not password or not hashed_password:
        return False
    return werkzeug.security.check_password_hash(hashed_password, password)
