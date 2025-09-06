Doctor-Patient Blog System

A Flask-based web application that allows doctors to upload blog posts for patients. Doctors can create, view, and manage their posts, while patients can read all published posts, categorized for easy access.

Features

Doctor Role:

Create new blog posts with fields: Title, Image, Category, Summary, Content.

Option to mark a post as draft.

View all posts uploaded by themselves.

Patient Role:

View all blog posts that are not marked as draft.

Posts are displayed category-wise.

Summary is truncated to 15 words followed by ... if longer.

View individual blog post details.

Categories: Example categories: Mental Health, Heart Disease, Covid19, Immunization.

Project Structure
          flask_role_blog/
          │
          ├── app.py                 # Main Flask application
          ├── models.py              # Database models (User, BlogPost, Category)
          ├── forms.py               # Flask-WTF forms (Login, Register, CreatePost)
          ├── config.py              # Configuration (DB URI, secret key)
          ├── static/
          │   └── uploads/           # Stores blog images
          ├── templates/             # HTML templates
          │   ├── base.html
          │   ├── login.html
          │   ├── register.html
          │   ├── doctor_dashboard.html
          │   ├── create_post.html
          │   ├── patient_dashboard.html
          │   └── view_post.html
          └── requirements.txt       # Python dependencies

Technologies Used

Backend: Python, Flask, Flask-WTF

Frontend: HTML, CSS, Bootstrap, optional JS libraries

Database: MySQL

ORM: Flask SQLAlchemy

Authentication & Roles: Flask-Login
