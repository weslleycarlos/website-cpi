# setup_admin.py
import os
import sys
from app import create_app, db
from app.models import Usuario
from datetime import datetime, timezone

def setup_admin():
    app = create_app()
    
    with app.app_context():
        # Verificar se admin já existe
        admin_exists = Usuario.query.filter_by(username='admin').first()
        if admin_exists:
            print("❌ Usuário admin já existe!")
            choice = input("Deseja resetar a senha? (s/n): ")
            if choice.lower() != 's':
                return
            
            new_password = input("Nova senha para admin: ")
            if not new_password:
                print("❌ Senha não pode ser vazia")
                return
                
            admin_exists.set_password(new_password)
            db.session.commit()
            print("✅ Senha do admin atualizada!")
            return
        
        # Criar novo admin
        print("👤 Criando usuário admin...")
        
        username = input("Username [admin]: ") or "admin"
        email = input("Email [admin@cpi.com]: ") or "admin@cpi.com"
        password = input("Senha: ")
        
        if not password:
            print("❌ Senha é obrigatória!")
            return
        
        admin_user = Usuario(
            username=username,
            email=email,
            is_active=True,
            date_created=datetime.now(timezone.utc)
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        print("   🔑 Senha: [definida]")

if __name__ == '__main__':
    setup_admin()