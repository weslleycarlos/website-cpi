# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # A configuração agora é simples: pega a DATABASE_URL do ambiente.
    # Localmente, ela virá do .env. No Render, virá das configurações do serviço.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # A lógica de semeadura pode ser removida daqui, pois faremos isso via comando
    # ou, no futuro, via painel de admin.

    return app