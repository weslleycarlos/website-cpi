# run.py
from app import create_app, db
from app.models import Usuario, Depoimento, Post, Evento

app = create_app()

@app.cli.command("seed-db")
def seed_db():
    """Semeia o banco de dados com dados iniciais para todas as tabelas."""
    print("Limpando tabelas antigas...")
    # A ordem importa por causa das chaves estrangeiras (deletar posts antes de usuários)
    db.session.query(Post).delete()
    db.session.query(Usuario).delete()
    db.session.query(Depoimento).delete()
    db.session.query(Evento).delete()

    print("Semeando usuário admin...")
    admin_user = Usuario(username='admin')
    admin_user.set_password('senhaforte123') # Troque por uma senha segura no futuro
    db.session.add(admin_user)
    
    # Precisamos commitar o usuário para que ele tenha um ID para ser usado nos posts
    db.session.commit()

    print("Semeando posts do blog...")
    posts = [
        Post(
            slug='5-dicas-para-comunicacao',
            title='5 Dicas para uma Comunicação Saudável no Casamento',
            summary='A comunicação é a base de tudo. Neste post, vamos explorar cinco dicas práticas para melhorar o diálogo com seu cônjuge...',
            content='Conteúdo completo do post sobre comunicação...',
            author_id=admin_user.id
        ),
        Post(
            slug='a-importancia-do-perdao',
            title='A Importância do Perdão na Vida a Dois',
            summary='Perdoar nem sempre é fácil, mas é essencial para a saúde do relacionamento. Descubra os princípios bíblicos do perdão...',
            content='Conteúdo completo do post sobre perdão...',
            author_id=admin_user.id
        )
    ]
    db.session.add_all(posts)

    print("Semeando depoimentos...")
    depoimentos = [
        Depoimento(quote="A mentoria do CPI foi um divisor de águas para nós...", author="João & Maria S."),
        Depoimento(quote="Estávamos quase desistindo, mas encontramos no CPI a esperança...", author="Pedro & Ana L.")
    ]
    db.session.add_all(depoimentos)

    db.session.commit()
    print("Banco de dados semeado com sucesso!")