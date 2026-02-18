# app/__init__.py
import os
from flask import Flask
# from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # CONFIGURAÇÕES DE SEGURANÇA
    # ===========================
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY não definida. Defina a variável de ambiente SECRET_KEY."
        )
    app.config['SECRET_KEY'] = secret_key

    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or \
        f'sqlite:///{os.path.join(os.path.dirname(__file__), "..", "site.db")}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

    # Segurança adicional
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.session_protection = 'strong'

    from .models import Usuario
    from datetime import datetime

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.context_processor
    def inject_globals():
        return {'current_year': datetime.now().year}

    # Registrar blueprints
    from .routes import main_bp
    from .admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Criar tabelas (somente em desenvolvimento)
    if os.environ.get('FLASK_ENV') != 'production':
        with app.app_context():
            db.create_all()

    return app