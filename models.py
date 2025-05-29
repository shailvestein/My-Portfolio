from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(900), nullable=False)
    from_date = db.Column(db.String(7), nullable=False)  # e.g., "2023-05"
    to_date = db.Column(db.String(7), nullable=False)
    accomplishments = db.Column(db.String(100), nullable=False)

class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.String(900), nullable=False)

class Skill(db.Model):
    __tablename__ = "skill"
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(100), nullable=False)

class Education(db.Model):
    __tablename__ = "education"
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    field = db.Column(db.String(100), nullable=False)
    from_date = db.Column(db.String(7), nullable=False)
    to_date = db.Column(db.String(7), nullable=False)
    percentage = db.Column(db.Float, nullable=False)

class Experience(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    from_date = db.Column(db.String(7), nullable=False)
    to_date = db.Column(db.String(7), nullable=False)
    accomplishments = db.Column(db.String(100), nullable=False)

class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(900), unique=True, nullable=False)
