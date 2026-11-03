from flask import Blueprint, render_template, flash, redirect, url_for, abort
from sqlalchemy import select
import datetime as dt
#own modules
from components.auth import login_required, current_user, admin_required
from components.forms import RequestPostForm, ActionForm, RejectForm
from components.models import PostRequest, BlogPost, STATUS_APPROVED, STATUS_PENDING, STATUS_REJECTED
from components.db import get_session
from components.app_utils import sanitize_html


requests_bp = Blueprint("requests_bp", __name__)

@requests_bp.route("/my-requests")
@login_required
def my_requests():
    mine = get_session().scalars(
        select(PostRequest)
        .where(PostRequest.author_id == current_user()["id"])
        .order_by(PostRequest.created_at.desc())
    ).all()
    return render_template("my_requests.html", requests=mine)

@requests_bp.route("/submit-post", methods=["GET", "POST"])
@login_required
def submit_post():
    form = RequestPostForm()
    if form.validate_on_submit():
        db_session = get_session()
        db_session.add(
            PostRequest(
                title=form.title.data,
                subtitle=form.subtitle.data,
                img_url=form.img_url.data,
                body=sanitize_html(form.body.data),
                author_id=current_user()["id"],
            )
        )
        db_session.commit()
        flash("Submitted! An admin will review it.")
        return redirect(url_for("requests_bp.submit_post"))
    return render_template("submit_post.html", form=form)

@requests_bp.route("/requests")
@admin_required
def review_list():
    db_session = get_session()
    pending = db_session.scalars(
        select(PostRequest)
        .where(PostRequest.status == STATUS_PENDING)
        .order_by(PostRequest.created_at)
    ).all()
    return render_template("requests.html", requests=pending, history=False)

@requests_bp.route("/requests/history")
@admin_required
def history():
    done = get_session().scalars(
        select(PostRequest)
        .where(PostRequest.status != STATUS_PENDING)
        .order_by(PostRequest.created_at.desc())
    ).all()
    return render_template("requests.html", requests=done, history=True)


@requests_bp.route("/requests/<int:req_id>")
@admin_required
def review_post(req_id):
    req = get_session().get(PostRequest, req_id)
    if req is None:
        abort(404)
    return render_template("review.html", req=req, action_form=ActionForm(), reject_form=RejectForm())


@requests_bp.route("/requests/<int:req_id>/approve", methods=["POST"])
@admin_required
def approve(req_id):
    db_session = get_session()
    req = db_session.get(PostRequest, req_id)
    if req is None:
        abort(404)
    if not ActionForm().validate_on_submit():
        abort(400)
    if req.status != STATUS_PENDING:       # blocks double-clicks
        flash("Already handled.")
        return redirect(url_for("requests_bp.review_list"))
    db_session.add(
        BlogPost(
            title=req.title,
            date=dt.datetime.now().strftime("%B %d, %Y"),
            body=req.body,
            author=req.author.name if req.author else "Unknown",
            img_url=req.img_url,
            subtitle=req.subtitle,
        )
    )
    req.status = STATUS_APPROVED
    db_session.commit()
    flash("Post Added!")
    return redirect(url_for("requests_bp.review_list"))


@requests_bp.route("/requests/<int:req_id>/reject", methods=["POST"])
@admin_required
def reject(req_id):
    db_session = get_session()
    form = RejectForm()
    req = db_session.get(PostRequest, req_id)
    if req is None:
        abort(404)
    if not form.validate_on_submit():
        abort(400)
    if req.status != STATUS_PENDING:       # blocks double-clicks
        flash("Already handled.")
        return redirect(url_for("requests_bp.review_list"))
    req.admin_note=form.admin_note.data or None
    req.status = STATUS_REJECTED
    db_session.commit()
    flash("Post Rejected!")
    return redirect(url_for("requests_bp.review_list"))
