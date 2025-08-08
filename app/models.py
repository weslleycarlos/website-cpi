# app/models.py
from . import db # Importa a instância 'db' do __init__.py

class Depoimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Depoimento {self.author}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), default='Equipe CPI')
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'