# app/routes.py
from flask import Blueprint, render_template
from datetime import datetime
from .models import Depoimento, Post # Importe seus models

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    current_year = datetime.now().year
    # BUSCA DO BANCO DE DADOS!
    depoimentos_db = Depoimento.query.order_by(Depoimento.id.desc()).all()
    
    return render_template('index.html', current_year=current_year, depoimentos=depoimentos_db)
# Adicione outras rotas aqui (como o futuro blog)