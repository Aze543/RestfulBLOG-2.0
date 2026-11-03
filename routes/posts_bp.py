
from flask import Blueprint, render_template, redirect, url_for, abort, request
import datetime as dt
from sqlalchemy import select, func
import math
#own modules
from components.db import get_session, get_post_or_404
from components.config import ADMIN_AVATAR
from components.forms import CommentForm, CreatePostForm, ActionForm
from components.auth import admin_required, current_user
from components.models import BlogPost, Comment
from components.app_utils import sanitize_html, clean_comment



posts = Blueprint("posts", __name__)

PER_PAGE = 5

@posts.route("/")
def get_all_posts():
    db_session = get_session()
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    total = db_session.scalar(select(func.count()).select_from(BlogPost))
    total_pages = max(1, math.ceil(total / PER_PAGE))
    if page > total_pages:
        page = total_pages

    page_posts = db_session.scalars(
        select(BlogPost)
        .order_by(BlogPost.id.desc())
        .limit(PER_PAGE)
        .offset((page - 1) * PER_PAGE)
    ).all()

    return render_template("index.html", all_posts=page_posts,
                           page=page, total_pages=total_pages, action_form=ActionForm())


@posts.route("/post/<int:index>", methods=["GET", "POST"])
def show_post(index):
    post = get_post_or_404(index)
    form = CommentForm()

    if form.validate_on_submit():
        db_session = get_session()
        user = current_user()
        if not user:
            return redirect(url_for("auth.register", first=1))

        cleaned = clean_comment(sanitize_html(form.comment.data))
        if not cleaned:
            return redirect(url_for("posts.show_post", index=index))

        db_session.add(
            Comment(
                title=post.title,
                comment=cleaned,
                name=user["name"],
                post_id=post.id,
                author_id=user["id"],
            )
        )
        db_session.commit()
        return redirect(url_for("posts.show_post", index=index))

    return render_template("post.html", post=post, form=form,
                           comments=post.comments, num=len(post.comments))


@posts.route("/new-post", methods=["GET", "POST"])
@admin_required
def add_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        db_session = get_session()
        db_session.add(
            BlogPost(
                title=form.title.data,
                date=dt.datetime.now().strftime("%B %d, %Y"),
                body=sanitize_html(form.body.data),
                author=form.author.data,
                img_url=form.img_url.data,
                subtitle=form.subtitle.data,
            )
        )
        db_session.commit()
        return redirect(url_for("posts.get_all_posts"))
    return render_template("make_post.html", form=form)


@posts.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    post = get_post_or_404(post_id)
    form = CreatePostForm(title=post.title, subtitle=post.subtitle, img_url=post.img_url,
                          author=post.author, body=post.body)
    if form.validate_on_submit():
        db_session = get_session()
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.author = form.author.data
        post.body = sanitize_html(form.body.data)
        db_session.commit()

        return redirect(url_for("posts.get_all_posts"))
    return render_template("make_post.html", form=form, edit=True)


@posts.route("/delete/<int:post_id>", methods=["POST"])
@admin_required
def delete_post(post_id):
    post = get_post_or_404(post_id)
    if not ActionForm().validate_on_submit():
        abort(400)
    db_session = get_session()
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for("posts.get_all_posts"))
