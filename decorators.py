from functools import wraps
from flask import abort

from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "Admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def admin_or_manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ["Admin", "Manager"]:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def analyst_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "Analyst":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
