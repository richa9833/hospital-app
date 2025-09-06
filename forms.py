from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("doctor", "Doctor"), ("patient", "Patient")], validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField("Category", choices=[("Mental Health", "Mental Health"),
                                                ("Heart Disease", "Heart Disease"),
                                                ("Covid19", "Covid19"),
                                                ("Immunization", "Immunization")],
                           validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    is_draft = BooleanField("Save as Draft")
    submit = SubmitField("Publish")
