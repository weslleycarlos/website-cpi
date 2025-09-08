# app/routes.py
from flask import Blueprint, render_template, abort
from datetime import datetime
from .models import Depoimento, Post

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    current_year = datetime.now().year
    depoimentos_db = Depoimento.query.filter_by(is_visible=True).order_by(Depoimento.id.desc()).all()
    return render_template('index.html', current_year=current_year, depoimentos=depoimentos_db)

# ROTA PARA A LISTAGEM DO BLOG
@main_bp.route('/blog')
def blog_list():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog_list.html', posts=posts)

# ROTA DINÂMICA PARA UM POST INDIVIDUAL
@main_bp.route('/blog/<string:slug>')
def blog_post(slug):
    # first_or_404 é uma função útil que busca o primeiro resultado ou retorna um erro 404
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog_post.html', post=post)