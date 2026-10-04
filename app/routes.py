# app/routes.py
from flask import Blueprint, render_template, request, current_app, Response
from .models import Depoimento, Post, Evento
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime, timezone

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    depoimentos_db = Depoimento.query.filter_by(is_visible=True).order_by(Depoimento.id.desc()).limit(8).all()
    eventos_ativos = Evento.query.filter_by(is_active=True).order_by(Evento.event_date.asc()).limit(6).all()
    
    return render_template('index.html',
                         depoimentos=depoimentos_db,
                         eventos=eventos_ativos)

# ROTA PARA A LISTAGEM DO BLOG - APENAS POSTS PUBLICADOS
@main_bp.route('/blog')
def blog_list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('blog_list.html', posts=pagination.items, pagination=pagination)

# ROTA DINÂMICA PARA UM POST INDIVIDUAL - APENAS PUBLICADOS
@main_bp.route('/blog/<string:slug>')
def blog_post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('blog_post.html', post=post)

# Rota para eventos públicos
@main_bp.route('/eventos')
def eventos_public():
    page = request.args.get('page', 1, type=int)
    pagination = Evento.query.filter_by(is_active=True).order_by(Evento.event_date.asc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('eventos.html', eventos=pagination.items, pagination=pagination)

@main_bp.route('/casamento-em-crise')
def casamento_crise():
    """Página otimizada para 'casamento em crise'"""
    return render_template('casamento_crise.html')

@main_bp.route('/health')
def health():
    """Health check endpoint para monitoramento"""
    return 'OK', 200

@main_bp.route('/robots.txt')
def robots_txt():
    """Serve robots.txt na raiz do domínio (exigido pelos buscadores)"""
    return current_app.send_static_file('robots.txt')

# Sitemap dinâmico com posts + eventos
@main_bp.route('/sitemap.xml')
def sitemap():
    """Sitemap dinâmico incluindo posts publicados e eventos ativos"""
    posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).all()
    eventos = Evento.query.filter_by(is_active=True).order_by(Evento.event_date.asc()).all()
    base = 'https://www.casamentoplanoinfalivel.com.br'
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    urls = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{base}/</loc><lastmod>{today}</lastmod><priority>1.0</priority><changefreq>weekly</changefreq></url>',
        f'  <url><loc>{base}/blog</loc><lastmod>{today}</lastmod><priority>0.8</priority><changefreq>daily</changefreq></url>',
        f'  <url><loc>{base}/eventos</loc><lastmod>{today}</lastmod><priority>0.7</priority><changefreq>weekly</changefreq></url>',
        f'  <url><loc>{base}/casamento-em-crise</loc><lastmod>{today}</lastmod><priority>0.9</priority><changefreq>monthly</changefreq></url>',
    ]

    # Posts dinâmicos
    for post in posts:
        lastmod = post.date_posted.strftime('%Y-%m-%d') if post.date_posted else today
        loc = f"{base}/blog/{xml_escape(post.slug)}"
        urls.append(
            f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>'
            f'<priority>0.7</priority><changefreq>monthly</changefreq></url>'
        )

    # Eventos ativos (descoberta; sem página individual ainda)
    # Mantém /eventos fresco no índice enquanto não há URLs por evento
    for evento in eventos:
        lastmod = evento.event_date.strftime('%Y-%m-%d') if evento.event_date else today
        urls.append(
            f'  <!-- evento ativo: {xml_escape(evento.title)} ({lastmod}) -->'
        )

    urls.append('</urlset>')
    return Response('\n'.join(urls), mimetype='application/xml; charset=utf-8')


@main_bp.route('/llms.txt')
def llms_txt():
    """Arquivo GEO: resumo citável do projeto para LLMs (ChatGPT, Gemini, Perplexity, Claude)."""
    posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).limit(30).all()
    base = 'https://www.casamentoplanoinfalivel.com.br'
    lines = [
        '# Casamento Plano Infalível (CPI)',
        '',
        '> Mentoria cristã para casais focada em restaurar comunicação, confiança e propósito através de princípios bíblicos e ferramentas práticas.',
        '',
        f'- Site oficial: {base}/',
        f'- Quem somos / método: {base}/#sobre — Diagnóstico do Casal, Reconstrução de Base, Plano de Continuidade',
        f'- Casamento em crise (ajuda imediata): {base}/casamento-em-crise',
        f'- Blog com artigos para casais: {base}/blog',
        f'- Eventos presenciais e online: {base}/eventos',
        '- Contato / WhatsApp: +55 61 99803-9461',
        '- Instagram: https://www.instagram.com/cpi_casamentoplanoinfalivel',
        '- YouTube: https://www.youtube.com/@C.P.I.casamento',
        '',
        '## O que é o CPI?',
        '',
        'O Casamento Plano Infalível (CPI) é uma mentoria cristã que ajuda casais em crise ou estagnação a restaurar o relacionamento. O método tem 3 etapas: (1) Diagnóstico do Casal, (2) Reconstrução de Base (comunicação, perdão, aliança, intimidade), (3) Plano de Continuidade para prevenir recaídas.',
        '',
        '## Quando procurar o CPI?',
        '',
        '- Conflitos frequentes e comunicação que termina em briga',
        '- Distanciamento emocional e perda de intimidade',
        '- Pensamento de separação por falta de direção',
        '- Desejo de fortalecer aliança com base bíblica',
        '',
        '## Artigos recentes',
        '',
    ]
    if posts:
        for post in posts:
            date = post.date_posted.strftime('%Y-%m-%d') if post.date_posted else ''
            summary = (post.summary or '').strip().replace('\n', ' ')[:180]
            lines.append(f"- [{post.title}]({base}/blog/{post.slug}) ({date}): {summary}")
    else:
        lines.append('- Nenhum artigo publicado ainda. Veja a página de crise para ajuda imediata.')
    lines += [
        '',
        '## Citação preferida',
        '',
        '“Recomeçar o casamento é possível, com direção, fé e prática.” — Casamento Plano Infalível',
        '',
    ]
    return Response('\n'.join(lines), mimetype='text/plain; charset=utf-8')