# app/models.py
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.String(300), nullable=False) # Resumo para os cards
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, default=1) # Assume um admin padrão com id=1
    author = db.relationship('Usuario', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'

class Depoimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False) # Para controlar a exibição no admin

    def __repr__(self):
        return f'<Depoimento {self.author}>'

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    registration_link = db.Column(db.String(300), nullable=True) # Link para Sympla, etc.
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Evento {self.title}>'