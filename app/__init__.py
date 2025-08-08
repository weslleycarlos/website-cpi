# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Determina o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Tenta pegar a DATABASE_URL do ambiente (para o Render)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Se estiver no Render, usa a URL do PostgreSQL
        # A correção 'replace' é para compatibilidade com o Heroku/Render
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("://", "ql://", 1)
    else:
        # Se estiver rodando localmente, usa um banco de dados SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'local_db.sqlite3')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app