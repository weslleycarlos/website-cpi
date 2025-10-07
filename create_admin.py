# create_admin.py (para produção)
import os
from app import create_app, db
from app.models import Usuario
from datetime import datetime, timezone

def create_production_admin():
    app = create_app()
    
    with app.app_context():
        # Verificar variáveis de ambiente
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@cpi.com')
        
        if not admin_password:
            raise ValueError("ADMIN_PASSWORD não definida no ambiente")
        
        # Verificar se admin já existe
        if Usuario.query.filter_by(username='admin').first():
            print("✅ Admin já existe")
            return
        
        # Criar admin
        admin_user = Usuario(
            username='admin',
            email=admin_email,
            is_active=True,
            date_created=datetime.now(timezone.utc)
        )
        admin_user.set_password(admin_password)
        
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin criado com sucesso!")

if __name__ == '__main__':
    create_production_admin()