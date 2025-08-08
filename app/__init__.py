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

    # --- INÍCIO DA SEÇÃO CORRIGIDA ---
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Se estiver no Render, usa a URL do PostgreSQL.
        # A correção agora é específica e segura: só troca 'postgres://' por 'postgresql://'
        # caso o Render forneça a URL no formato antigo.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Se estiver rodando localmente, usa um banco de dados SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'local_db.sqlite3')
    # --- FIM DA SEÇÃO CORRIGIDA ---

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    # --- INÍCIO DA LÓGICA DE SEMEADURA AUTOMÁTICA ---
    with app.app_context():
        from .models import Depoimento, Post
        
        # Cria as tabelas se não existirem (alternativa segura se db upgrade falhar)
        db.create_all() 

        # Verifica se a tabela Depoimento está vazia
        if Depoimento.query.count() == 0:
            print("Tabela de depoimentos vazia, semeando dados...")
            depoimentos = [
                Depoimento(quote="A mentoria do CPI foi um divisor de águas para nós...", author="João & Maria S."),
                Depoimento(quote="Estávamos quase desistindo, mas encontramos no CPI a esperança...", author="Pedro & Ana L."),
                Depoimento(quote="Como noivos, fazer a mentoria nos deu uma base sólida...", author="Lucas & Gabriela F.")
            ]
            for d in depoimentos:
                db.session.add(d)
            db.session.commit()
            print("Depoimentos semeados.")

        # Pode adicionar lógica similar para os Posts
        if Post.query.count() == 0:
             print("Tabela de posts vazia, semeando dados...")
             # Adicione a criação dos seus posts aqui
             # posts = [ Post(...), Post(...) ]
             # db.session.add_all(posts)
             # db.session.commit()
             print("Posts semeados.")

    # --- FIM DA LÓGICA DE SEMEADURA ---




    return app