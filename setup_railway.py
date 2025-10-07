# setup_railway.py
import os
import sys
from app import create_app, db
from app.models import Usuario, Depoimento, Post, Evento
from datetime import datetime, timezone

def setup_railway():
    app = create_app()
    
    with app.app_context():
        print("🚂 Configurando banco no Railway...")
        
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar/Criar usuário admin
        admin_exists = Usuario.query.filter_by(username='admin').first()
        admin_user = None
        
        if not admin_exists:
            print("👤 Criando usuário admin...")
            admin_password = os.environ.get('ADMIN_PASSWORD')
            
            if not admin_password:
                print("❌ ERRO: ADMIN_PASSWORD não configurada")
                print("💡 Configure no painel do Railway: ADMIN_PASSWORD=sua-senha-forte")
                sys.exit(1)
            
            admin_user = Usuario(
                username='admin',
                email=os.environ.get('ADMIN_EMAIL', 'weslley.unemat@gmail.com'),
                is_active=True,
                date_created=datetime.now(timezone.utc)
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            print("✅ Admin criado com sucesso!")
        else:
            admin_user = admin_exists
            print("✅ Admin já existe")
        
        # Adicionar posts se não existirem
        if Post.query.count() == 0:
            print("📝 Adicionando posts de exemplo...")
            posts = [
                Post(
                    slug='alicerce-divino-casamento-forte',
                    title='O Alicerce Divino para um Casamento Forte',
                    summary='Descubra como os princípios bíblicos podem transformar seu casamento em uma construção sólida e duradoura.',
                    content='<h2>A Parábola do Construtor Sábio</h2><p>"Todo aquele, pois, que ouve estas minhas palavras e as põe em prática será comparado a um homem prudente, que edificou a casa sobre a rocha..."</p>',
                    is_published=True,
                    author_id=admin_user.id
                ),
                Post(
                    slug='poder-perdão-vida-conjugal',
                    title='O Poder do Perdão na Vida Conjugal',
                    summary='Explore como o perdão bíblico pode restaurar relacionamentos e trazer renovação espiritual.',
                    content='<h2>Uma Escolha que Liberta</h2><p>O perdão não é apenas um conceito bonito - é uma necessidade espiritual e emocional...</p>',
                    is_published=True,
                    author_id=admin_user.id
                )
            ]
            db.session.add_all(posts)
            print("✅ Posts criados!")
        
        # Adicionar depoimentos se não existirem
        if Depoimento.query.count() == 0:
            print("💬 Adicionando depoimentos...")
            depoimentos = [
                Depoimento(
                    quote="A mentoria do CPI foi um divisor de águas para nós. Aprendemos a dialogar em vez de brigar e a colocar Deus no centro de tudo.",
                    author="João & Maria S.",
                    is_visible=True
                ),
                Depoimento(
                    quote="Estávamos quase desistindo, mas encontramos no CPI a esperança e as ferramentas que precisávamos. Hoje nosso casamento é mais forte.",
                    author="Pedro & Ana L.", 
                    is_visible=True
                )
            ]
            db.session.add_all(depoimentos)
            print("✅ Depoimentos criados!")
        
        db.session.commit()
        print("🎉 Setup Railway concluído!")
        print(f"📊 Estatísticas:")
        print(f"   👤 Usuários: {Usuario.query.count()}")
        print(f"   📝 Posts: {Post.query.count()}")
        print(f"   💬 Depoimentos: {Depoimento.query.count()}")

if __name__ == '__main__':
    setup_railway()