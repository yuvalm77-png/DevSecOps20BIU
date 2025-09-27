from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, create_access_token
import hashlib, base64

def verify_scrypt(stored, password):
    # stored = scrypt:32768:8:1$salt$hash
    try:
        _, salt, hashval = stored.split('$')
        salt_bytes = salt.encode()
        hashed = hashlib.scrypt(password.encode(), salt=salt_bytes, n=32768, r=8, p=1)
        return base64.b16encode(hashed).lower() == hashval.encode()
    except Exception as e:
        print(f"verify_scrypt error: {e}")
        return False

def admin_required(fn):
    """Decorator that ensures the requester is an admin."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        print(f"DEBUG: Claims in admin_required: {claims}")
        print(f"DEBUG: is_admin claim: {claims.get('is_admin', False)}")
        if not claims.get('is_admin', False):
            return jsonify({"error": "Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper

def generate_admin_token(user_id):
    """Create JWT for admin user with is_admin claim."""
    return create_access_token(identity=user_id, additional_claims={"is_admin": True})
