# app/admin_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import Post, Depoimento, Usuario, Evento
from datetime import datetime, timezone
from urllib.parse import urlparse
import bleach

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Configuração de sanitização HTML
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'hr', 'div', 'span'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title']
}

def validate_password(password):
    """Valida força da senha"""
    if not password:
        return False, "Senha é obrigatória"
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    if not any(c.isupper() for c in password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"
    if not any(c.islower() for c in password):
        return False, "Senha deve conter pelo menos uma letra minúscula"
    if not any(c.isdigit() for c in password):
        return False, "Senha deve conter pelo menos um número"
    return True, ""

def sanitize_html(content):
    """Sanitiza conteúdo HTML"""
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

def normalize_external_url(raw_url):
    """Aceita apenas URLs externas com protocolo HTTP/HTTPS."""
    if not raw_url:
        return None

    value = raw_url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in ('http', 'https'):
        return None
    return value

def get_page_number():
    """Obtém o número da página atual para paginação."""
    return request.args.get('page', 1, type=int)

# Rota de login
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Usuário e senha são obrigatórios.', 'error')
            return render_template('admin/login.html'), 400
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Usuário desativado. Contate outro administrador.', 'error')
                return render_template('admin/login.html'), 403

            if not login_user(user):
                flash('Não foi possível iniciar a sessão.', 'error')
                return render_template('admin/login.html'), 401

            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('admin.login'))

# Dashboard
@admin_bp.route('/')
@login_required
def dashboard():
    posts_count = Post.query.count()
    published_posts = Post.query.filter_by(is_published=True).count()
    depoimentos_count = Depoimento.query.count()
    eventos_count = Evento.query.count()
    
    return render_template('admin/dashboard.html', 
                         posts_count=posts_count,
                         published_posts=published_posts,
                         depoimentos_count=depoimentos_count,
                         eventos_count=eventos_count)

# Gestão de Posts
@admin_bp.route('/posts')
@login_required
def posts():
    page = get_page_number()
    pagination = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/posts.html', posts=pagination.items, pagination=pagination)

@admin_bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        slug = request.form.get('slug')
        title = request.form.get('title')
        summary = request.form.get('summary')
        content = sanitize_html(request.form.get('content'))  # Sanitizar HTML
        is_published = 'is_published' in request.form
        
        # Verificar se o slug já existe
        existing_post = Post.query.filter_by(slug=slug).first()
        if existing_post:
            flash('Já existe um post com este slug. Escolha outro.', 'error')
            return render_template('admin/edit_post.html')
        
        new_post = Post(
            slug=slug,
            title=title,
            summary=summary,
            content=content,
            is_published=is_published,
            author_id=current_user.id
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('admin.posts'))
    
    return render_template('admin/edit_post.html')

@admin_bp.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        new_slug = request.form.get('slug')
        
        # Verificar se slug mudou e se já existe
        if new_slug != post.slug:
            existing = Post.query.filter_by(slug=new_slug).first()
            if existing:
                flash('Já existe um post com este slug. Escolha outro.', 'error')
                return render_template('admin/edit_post.html', post=post)
        
        post.slug = new_slug
        post.title = request.form.get('title')
        post.summary = request.form.get('summary')
        post.content = sanitize_html(request.form.get('content'))  # Sanitizar HTML
        post.is_published = 'is_published' in request.form
        
        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('admin.posts'))
    
    return render_template('admin/edit_post.html', post=post)

@admin_bp.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deletado com sucesso!', 'success')
    return redirect(url_for('admin.posts'))

# Gestão de Depoimentos - ROTAS ATUALIZADAS
@admin_bp.route('/depoimentos')
@login_required
def depoimentos():
    page = get_page_number()
    pagination = Depoimento.query.order_by(Depoimento.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/depoimentos.html', depoimentos=pagination.items, pagination=pagination)

@admin_bp.route('/depoimentos/new', methods=['GET', 'POST'])
@login_required
def new_depoimento():
    if request.method == 'POST':
        quote = request.form.get('quote')
        author = request.form.get('author')
        is_visible = 'is_visible' in request.form
        
        new_depoimento = Depoimento(quote=quote, author=author, is_visible=is_visible)
        db.session.add(new_depoimento)
        db.session.commit()
        flash('Depoimento adicionado com sucesso!', 'success')
        return redirect(url_for('admin.depoimentos'))
    
    return render_template('admin/edit_depoimento.html')

@admin_bp.route('/depoimentos/edit/<int:depoimento_id>', methods=['GET', 'POST'])
@login_required
def edit_depoimento(depoimento_id):
    depoimento = Depoimento.query.get_or_404(depoimento_id)
    
    if request.method == 'POST':
        depoimento.quote = request.form.get('quote')
        depoimento.author = request.form.get('author')
        depoimento.is_visible = 'is_visible' in request.form
        
        db.session.commit()
        flash('Depoimento atualizado com sucesso!', 'success')
        return redirect(url_for('admin.depoimentos'))
    
    return render_template('admin/edit_depoimento.html', depoimento=depoimento)

@admin_bp.route('/depoimentos/delete/<int:depoimento_id>', methods=['POST'])
@login_required
def delete_depoimento(depoimento_id):
    depoimento = Depoimento.query.get_or_404(depoimento_id)
    db.session.delete(depoimento)
    db.session.commit()
    flash('Depoimento deletado com sucesso!', 'success')
    return redirect(url_for('admin.depoimentos'))

# Gestão de Eventos
@admin_bp.route('/eventos')
@login_required
def eventos():
    page = get_page_number()
    pagination = Evento.query.order_by(Evento.event_date.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/eventos.html', eventos=pagination.items, pagination=pagination)

@admin_bp.route('/eventos/new', methods=['GET', 'POST'])
@login_required
def new_evento():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        event_date_str = request.form.get('event_date')
        location = request.form.get('location', '').strip()
        raw_registration_link = request.form.get('registration_link')
        registration_link = normalize_external_url(raw_registration_link)
        is_active = 'is_active' in request.form

        if raw_registration_link and not registration_link:
            flash('Link de inscrição inválido. Use apenas URLs http/https.', 'error')
            return render_template('admin/edit_evento.html')
        
        # Converter string para datetime com tratamento de erro
        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            flash('Data/hora inválida. Use o formato correto (YYYY-MM-DD HH:MM).', 'error')
            return render_template('admin/edit_evento.html')
        
        new_evento = Evento(
            title=title,
            description=description,
            event_date=event_date,
            location=location,
            registration_link=registration_link,
            is_active=is_active
        )
        
        db.session.add(new_evento)
        db.session.commit()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('admin.eventos'))
    
    return render_template('admin/edit_evento.html')

@admin_bp.route('/eventos/edit/<int:evento_id>', methods=['GET', 'POST'])
@login_required
def edit_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    
    if request.method == 'POST':
        evento.title = request.form.get('title', '').strip()
        evento.description = request.form.get('description', '').strip()
        event_date_str = request.form.get('event_date')
        evento.location = request.form.get('location', '').strip()
        raw_registration_link = request.form.get('registration_link')
        registration_link = normalize_external_url(raw_registration_link)
        if raw_registration_link and not registration_link:
            flash('Link de inscrição inválido. Use apenas URLs http/https.', 'error')
            return render_template('admin/edit_evento.html', evento=evento)
        evento.registration_link = registration_link
        evento.is_active = 'is_active' in request.form
        
        # Converter string para datetime com tratamento de erro
        try:
            evento.event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            flash('Data/hora inválida. Use o formato correto (YYYY-MM-DD HH:MM).', 'error')
            return render_template('admin/edit_evento.html', evento=evento)
        
        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('admin.eventos'))
    
    return render_template('admin/edit_evento.html', evento=evento)

@admin_bp.route('/eventos/delete/<int:evento_id>', methods=['POST'])
@login_required
def delete_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento deletado com sucesso!', 'success')
    return redirect(url_for('admin.eventos'))


# Gestão de Usuários
@admin_bp.route('/usuarios')
@login_required
def usuarios():
    page = get_page_number()
    pagination = Usuario.query.order_by(Usuario.date_created.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/usuarios.html', usuarios=pagination.items, pagination=pagination)

@admin_bp.route('/usuarios/new', methods=['GET', 'POST'])
@login_required
def new_usuario():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações
        if not username or not password:
            flash('Username e senha são obrigatórios.', 'error')
            return render_template('admin/edit_usuario.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('admin/edit_usuario.html')
        
        # Validar força da senha
        is_valid, msg = validate_password(password)
        if not is_valid:
            flash(msg, 'error')
            return render_template('admin/edit_usuario.html')
        
        # Verificar se username já existe
        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user:
            flash('Já existe um usuário com este username.', 'error')
            return render_template('admin/edit_usuario.html')
        
        # Verificar se email já existe (se fornecido)
        if email:
            existing_email = Usuario.query.filter_by(email=email).first()
            if existing_email:
                flash('Já existe um usuário com este email.', 'error')
                return render_template('admin/edit_usuario.html')
        
        # Criar novo usuário
        new_user = Usuario(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/edit_usuario.html')

@admin_bp.route('/usuarios/edit/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def edit_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # Impedir que o usuário edite a si mesmo (opcional)
    if usuario.id == current_user.id:
        flash('Você não pode editar seu próprio usuário por aqui.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    if request.method == 'POST':
        usuario.username = request.form.get('username')
        usuario.email = request.form.get('email')
        usuario.is_active = 'is_active' in request.form
        
        # Reset de senha (se fornecido)
        new_password = request.form.get('new_password')
        if new_password:
            confirm_password = request.form.get('confirm_password')
            if new_password != confirm_password:
                flash('As senhas não coincidem.', 'error')
                return render_template('admin/edit_usuario.html', usuario=usuario)
            
            # Validar força da senha
            is_valid, msg = validate_password(new_password)
            if not is_valid:
                flash(msg, 'error')
                return render_template('admin/edit_usuario.html', usuario=usuario)
            
            usuario.set_password(new_password)
            flash('Senha resetada com sucesso!', 'success')
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/edit_usuario.html', usuario=usuario)

@admin_bp.route('/usuarios/reset-password/<int:usuario_id>', methods=['POST'])
@login_required
def reset_password(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if usuario.id == current_user.id:
        flash('Você não pode resetar sua própria senha por aqui.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not new_password:
        flash('A nova senha é obrigatória.', 'error')
        return redirect(url_for('admin.edit_usuario', usuario_id=usuario_id))
    
    if new_password != confirm_password:
        flash('As senhas não coincidem.', 'error')
        return redirect(url_for('admin.edit_usuario', usuario_id=usuario_id))

    is_valid, msg = validate_password(new_password)
    if not is_valid:
        flash(msg, 'error')
        return redirect(url_for('admin.edit_usuario', usuario_id=usuario_id))
    
    usuario.set_password(new_password)
    db.session.commit()
    flash('Senha resetada com sucesso!', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios/toggle-active/<int:usuario_id>', methods=['POST'])
@login_required
def toggle_active_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if usuario.id == current_user.id:
        flash('Você não pode desativar seu próprio usuário.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    usuario.is_active = not usuario.is_active
    status = "ativado" if usuario.is_active else "desativado"
    db.session.commit()
    flash(f'Usuário {status} com sucesso!', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios/delete/<int:usuario_id>', methods=['POST'])
@login_required
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if usuario.id == current_user.id:
        flash('Você não pode deletar seu próprio usuário.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    # Verificar se o usuário tem posts (opcional - para evitar deletar usuários com conteúdo)
    if usuario.posts:
        flash('Não é possível deletar usuários que possuem posts.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('admin.usuarios'))