from flask import Blueprint, render_template, redirect, url_for, flash
import datetime as dt
import smtplib
from email.message import EmailMessage
#own modules
from components.config import SENDER_EMAIL, SENDER_EMAIL_PW, RECEIVER_EMAIL
from components.forms import ContactForm
from components.auth import login_required

pages = Blueprint("pages", __name__)

@pages.route("/about")
def about():
    return render_template("about.html")


def send_inquiry(form):
    msg = EmailMessage()
    msg["Subject"] = f"Blog inquiry from {form.name.data}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Reply-To"] = form.email.data
    msg.set_content(
        f"Name: {form.name.data}\n"
        f"Email: {form.email.data}\n"
        f"Date: {dt.datetime.now():%B %d, %Y}\n\n"
        f"{form.message.data}\n"
    )
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=SENDER_EMAIL_PW)
        connection.send_message(msg)


@pages.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_inquiry(form)
        flash("Thanks! I'll get back to you as soon as possible.")
        return redirect(url_for("pages.contact"))
    return render_template("contact.html", form=form)
