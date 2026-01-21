# app/__init__.py
import os
from flask import Flask
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # CONFIGURAÇÕES DE SEGURANÇA
    # ===========================
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY must be set in production environment")
        secret_key = 'dev-key-change-in-production'
    app.config['SECRET_KEY'] = secret_key

    # Configurações de segurança
    csp = {
        'default-src': [
            "'self'",
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com'
        ],
        'script-src': [
            "'self'",
            'https://www.googletagmanager.com',
            'https://www.google-analytics.com'
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",  # Necessário para alguns estilos
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com'
        ],
        'font-src': [
            "'self'",
            'https://cdnjs.cloudflare.com',
            'https://fonts.gstatic.com'
        ],
        'connect-src': [
            "'self'",
            'https://www.google-analytics.com',
            'https://analytics.google.com'
        ]
    }

    Talisman(
        app,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        force_https=os.environ.get('FLASK_ENV') == 'production',
        strict_transport_security=True,
        session_cookie_secure=True,
        session_cookie_http_only=True
    )

    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Se for SQLite relativo, converte para caminho absoluto (evita criar em instance/)
    if database_url and database_url.startswith('sqlite:///'):
        db_path = database_url.replace('sqlite:///', '', 1)
        if not os.path.isabs(db_path):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            database_url = f"sqlite:///{os.path.join(base_dir, db_path)}"

    # Padrão: sqlite na raiz do projeto
    if not database_url:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        database_url = f'sqlite:///{os.path.join(base_dir, "site.db")}'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

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
    csrf.init_app(app)

    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.session_protection = 'strong'

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from .routes import main_bp
    from .admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Garantir que a nonce CSP está disponível antes de renderizar qualquer template
    @app.before_request
    def ensure_csp_nonce():
        from flask import g
        from secrets import token_hex
        if 'csp_nonce' not in g:
            g.csp_nonce = token_hex(16)

    # Configurar logging
    if os.environ.get('FLASK_ENV') == 'production':
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Log de aplicação
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cpi_app.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CPI Application startup')
    
    # Error handlers
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500

    # Criar tabelas (somente em desenvolvimento)
    if os.environ.get('FLASK_ENV') != 'production':
        with app.app_context():
            db.create_all()

    return app