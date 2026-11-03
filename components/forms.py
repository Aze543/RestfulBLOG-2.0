from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import URL, DataRequired, Length, Optional, Email
from flask_wtf import FlaskForm

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired(), Length(max=250)])
    subtitle = StringField("Subtitle", validators=[DataRequired(), Length(max=250)])
    author = StringField("Your Name", validators=[DataRequired(), Length(max=250)])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterBlogForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=250)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=250)])
    name = StringField("Name", validators=[DataRequired(), Length(max=250)])
    submit = SubmitField("Submit")

class LoginBlogForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=250)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=250)])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):
    name = StringField("Display Name", validators=[DataRequired(), Length(max=250)])
    image = StringField("Profile Image URL", validators=[Optional(), URL(), Length(max=250)])
    submit = SubmitField("Save Changes")

class RequestPostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired(), Length(max=250)])
    subtitle = StringField("Subtitle", validators=[DataRequired(), Length(max=250)])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Post Content", validators=[DataRequired()])
    submit = SubmitField("Submit for Review")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Your Email", validators=[DataRequired(), Email(), Length(max=250)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send")

class ActionForm(FlaskForm):
    submit = SubmitField("Submit")

class RejectForm(FlaskForm):
    admin_note = TextAreaField("Reason", validators=[Optional(), Length(max=1000)])
