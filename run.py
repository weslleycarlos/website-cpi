from app import create_app, db
from app.models import Usuario, Depoimento, Post, Evento
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import sys
import traceback

load_dotenv()  # Carrega variáveis do arquivo .env

try:
    app = create_app()
    print("✅ App criado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao criar app: {e}")
    traceback.print_exc()
    sys.exit(1)

@app.cli.command("seed-db")
def seed_db():
    """Semeia o banco de dados com dados iniciais - APENAS PARA DESENVOLVIMENTO"""
    if os.environ.get('FLASK_ENV') == 'production':
        print("❌ ERRO: Não execute seed-db em produção!")
        return
    with app.app_context():
        # VERIFICAR SE JÁ EXISTE ADMIN antes de deletar qualquer coisa
        admin_exists = Usuario.query.filter_by(username='admin').first()
        if admin_exists:
            print("✅ Usuário admin já existe. Pulando seed...")
            return

        print("🗑️  Limpando tabelas antigas...")
        # A ordem importa por causa das chaves estrangeiras
        db.session.query(Post).delete()
        db.session.query(Depoimento).delete()
        db.session.query(Evento).delete()
        db.session.query(Usuario).delete()
            
        print("👤 Criando usuário admin...")
        
        # SENHA DEVE VIR DO AMBIENTE
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if not admin_password:
            print("❌ ERRO: ADMIN_PASSWORD não configurada no ambiente")
            print("💡 Defina a variável ADMIN_PASSWORD no seu .env")
            return
        admin_user = Usuario(
            username='admin', 
            email=os.environ.get('ADMIN_EMAIL', 'weslley.unemat@gmail.com'),
            is_active=True,
            date_created=datetime.now(timezone.utc)
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()

        print("📝 Semando posts do blog...")
        posts = [
            Post(
                slug='5-dicas-para-comunicacao',
                title='5 Dicas para uma Comunicação Saudável no Casamento',
                summary='A comunicação é a base de tudo...',
                content='Conteúdo completo...',
                is_published=True,
                author_id=admin_user.id
            ),
            Post(
                slug='a-importancia-do-perdao',
                title='A Importância do Perdão na Vida a Dois',
                summary='Perdoar nem sempre é fácil...',
                content='Conteúdo completo...',
                is_published=True,
                author_id=admin_user.id
            )
        ]
        db.session.add_all(posts)

        print("💬 Semando depoimentos...")
        depoimentos = [
            Depoimento(quote="A mentoria do CPI foi um divisor de águas para nós...", author="João & Maria S."),
            Depoimento(quote="Estávamos quase desistindo, mas encontramos no CPI a esperança...", author="Pedro & Ana L.")
        ]
        db.session.add_all(depoimentos)

        db.session.commit()
        print("✅ Banco de dados semeado com sucesso!")
        


@app.route('/health')
def health():
    return 'OK', 200

# Configuração para produção
if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 Iniciando servidor na porta {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        traceback.print_exc()