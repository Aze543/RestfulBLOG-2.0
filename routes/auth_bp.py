from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
from flask import flash
#own modules
from components.forms import RegisterBlogForm, LoginBlogForm, ProfileForm
from components.config import ADMIN_EMAIL, ADMIN_AVATAR
from components.db import get_session
from components.auth import current_user, login_required
from components.models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterBlogForm()
    if form.validate_on_submit():
        db_session = get_session()
        email = form.email.data.strip().lower()
        if db_session.scalar(select(User).where(User.email == email)):
            return redirect(url_for("auth.login", exist=1))
        is_admin = email == (ADMIN_EMAIL or "").lower()
        user = User(
            email=email,
            password=generate_password_hash(form.password.data),
            name=form.name.data,
            image=ADMIN_AVATAR if is_admin else None,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        session["user"] = dict(id=user.id, name="Admin" if is_admin else user.name, is_admin=is_admin)
        return redirect(url_for("posts.get_all_posts"))

    return render_template("register.html", form=form,
                           first=request.args.get("first"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginBlogForm()
    error = False
    if form.validate_on_submit():
        db_session = get_session()
        email = form.email.data.strip().lower()
        user = db_session.scalar(select(User).where(User.email == email))
        if user and check_password_hash(user.password, form.password.data):
            is_admin = email == (ADMIN_EMAIL or "").lower()
            session["user"] = dict(id=user.id,
                                   name="Admin" if is_admin else user.name,
                                   is_admin=is_admin)
            return redirect(url_for("posts.get_all_posts"))
        error = True

    return render_template("login.html", form=form, msg=error,
                           exist=request.args.get("exist"))


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db_session = get_session()
    user = db_session.get(User, current_user()["id"])
    if user is None:                       # account no longer exists
        session.pop("user", None)
        return redirect(url_for("auth.login"))

    form = ProfileForm(obj=user)           # pre-fills name and image from the User
    if form.validate_on_submit():
        user.name = form.name.data.strip()
        user.image = form.image.data.strip() or None
        db_session.commit()

        is_admin = current_user()["is_admin"]
        session["user"] = dict(id=user.id,
                               name="Admin" if is_admin else user.name,
                               is_admin=is_admin)

        flash("Profile updated!")
        return redirect(url_for("auth.profile"))

    return render_template("profile.html", form=form, profile_user=user)


@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("posts.get_all_posts"))
