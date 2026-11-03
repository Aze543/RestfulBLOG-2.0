from flask import session, redirect, url_for, request
import datetime as dt
from functools import wraps
from sqlalchemy import select, func
#owwn modules
from components.db import get_session
from components.models import PostRequest, STATUS_PENDING

def current_user():
    return session.get("user")


def is_admin():
    user = current_user()
    return bool(user and user["is_admin"])


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            return redirect(url_for("auth.register", first=1))
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not is_admin():
            return "<p>You don't have access to this site.</p>", 403
        return view(*args, **kwargs)
    return wrapper


def inject_state():
    """Gives every template the flags it used to receive from the globals."""
    user = current_user()
    pending_count = 0
    if is_admin():
        pending_count = get_session().scalar(
                   select(func.count())
                   .select_from(PostRequest)
                   .where(PostRequest.status == STATUS_PENDING)
               )
    return dict(
        logged=bool(user),
        out=not user,
        user=bool(user),
        user_name=user["name"] if user else None,
        admin=is_admin(),
        in_reg=request.endpoint == "auth.register",
        in_log=request.endpoint == "auth.login",
        current_year=dt.datetime.now().year,
        pending_count=pending_count,
    )
