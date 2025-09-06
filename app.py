import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, BlogPost
from forms import RegistrationForm, LoginForm, BlogPostForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    if not hasattr(app, '_db_initialized'):
        db.create_all()
        app._db_initialized = True


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("doctor_dashboard" if user.role == "doctor" else "patient_dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/doctor/dashboard")
@login_required
def doctor_dashboard():
    if current_user.role != "doctor":
        return redirect(url_for("patient_dashboard"))
    posts = BlogPost.query.filter_by(user_id=current_user.id).all()
    return render_template("doctor_dashboard.html", posts=posts)

@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if current_user.role != "doctor":
        return redirect(url_for("patient_dashboard"))
    form = BlogPostForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = BlogPost(
            title=form.title.data,
            image=filename,
            category=form.category.data,
            summary=form.summary.data,
            content=form.content.data,
            is_draft=form.is_draft.data,
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("doctor_dashboard"))
    return render_template("create_post.html", form=form)

@app.route("/patient/dashboard")
@login_required
def patient_dashboard():
    if current_user.role != "patient":
        return redirect(url_for("doctor_dashboard"))
    posts = BlogPost.query.filter_by(is_draft=False).all()
    return render_template("patient_dashboard.html", posts=posts)

@app.route("/post/<int:post_id>")
@login_required
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("view_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)

