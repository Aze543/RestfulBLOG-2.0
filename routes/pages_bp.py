from flask import Blueprint, render_template, redirect, url_for, flash
import datetime as dt
import smtplib
from email.message import EmailMessage
#own modules
from components.config import SENDER_EMAIL, SENDER_EMAIL_PW, RECEIVER_EMAIL, RESEND_API_KEY
from components.forms import ContactForm
from components.auth import login_required
import resend

pages = Blueprint("pages", __name__)
resend.api_key = RESEND_API_KEY

@pages.route("/about")
def about():
    return render_template("about.html")


def send_inquiry(form):
    resend.Emails.send({
        "subject": f"Blog inquiry from {form.name.data}",
        "from": SENDER_EMAIL,
        "to": [RECEIVER_EMAIL],
        "reply_to": form.email.data,
        "text": (
            f"Name: {form.name.data}\n"
            f"Email: {form.email.data}\n"
            f"Date: {dt.datetime.now():%B %d, %Y}\n\n"
            f"{form.message.data}\n"
        ),
    })



@pages.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_inquiry(form)
        flash("Thanks! I'll get back to you as soon as possible.")
        return redirect(url_for("pages.contact"))
    return render_template("contact.html", form=form)
