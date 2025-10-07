# app/routes.py
from flask import Blueprint, render_template, abort
from datetime import datetime
from .models import Depoimento, Post, Evento

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    current_year = datetime.now().year
    depoimentos_db = Depoimento.query.filter_by(is_visible=True).order_by(Depoimento.id.desc()).all()
    eventos_ativos = Evento.query.filter_by(is_active=True).order_by(Evento.event_date.asc()).all()
    
    return render_template('index.html', 
                         current_year=current_year, 
                         depoimentos=depoimentos_db,
                         eventos=eventos_ativos)

# ROTA PARA A LISTAGEM DO BLOG - APENAS POSTS PUBLICADOS
@main_bp.route('/blog')
def blog_list():
    posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).all()
    return render_template('blog_list.html', posts=posts)

# ROTA DINÂMICA PARA UM POST INDIVIDUAL - APENAS PUBLICADOS
@main_bp.route('/blog/<string:slug>')
def blog_post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('blog_post.html', post=post)

# Rota para eventos públicos
@main_bp.route('/eventos')
def eventos_public():
    eventos = Evento.query.filter_by(is_active=True).order_by(Evento.event_date.asc()).all()
    return render_template('eventos.html', eventos=eventos)
