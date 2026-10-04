"""Render public templates with isolated data: python -m unittest discover -s tests."""
import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from bs4 import BeautifulSoup
from flask import render_template

from app import create_app, db
from app.models import Depoimento, Evento, Post, Usuario


def seed_content():
    author = Usuario(username='Equipe de teste')
    author.set_password('Frontend-test-only-123!')
    db.session.add(author)
    db.session.flush()
    for index in range(10):
        db.session.add(Post(
            title=f'Reflexão {index}: o cuidado na vida a dois',
            slug=f'reflexao-{index}',
            summary='Pequenos gestos abrem espaço para uma boa conversa.',
            content='<h2>Um tempo para ouvir</h2><p>Uma reflexão de teste.</p>'
                    '<blockquote>Cultive a presença.</blockquote>',
            author_id=author.id, is_published=True,
            date_posted=datetime(2026, 10, index + 1),
        ))
    db.session.add(Post(title='Rascunho privado', slug='rascunho-privado',
                        summary='Privado', content='Não publicar',
                        author_id=author.id, is_published=False))
    for index in range(11):
        db.session.add(Evento(
            title=f'Encontro {index}: tempo de reconectar',
            description='Um encontro para conversar, aprender e caminhar juntos.',
            event_date=datetime(2026, 10, index + 1, 19, 30),
            location='Encontro online',
            registration_link='https://example.com/inscricao', is_active=True,
        ))
    db.session.add(Evento(title='Evento inativo', description='Privado',
                          event_date=datetime(2026, 10, 20), location='Local',
                          is_active=False))
    db.session.add_all([
        Depoimento(author='Casal de teste', quote='Depoimento de teste visível.'),
        Depoimento(author='Casal privado', quote='Depoimento oculto.', is_visible=False),
    ])
    db.session.commit()


class PublicFrontendTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='cpi-ui-test-')
        uri = 'sqlite:///' + (Path(self.directory.name) / 'test.db').as_posix()
        with patch.dict(os.environ, {
            'SECRET_KEY': 'isolated-frontend-test-only',
            'FLASK_ENV': 'development', 'DATABASE_URL': uri,
        }):
            self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.directory.cleanup()

    def page(self, path, status=200):
        response = self.client.get(path)
        self.assertEqual(response.status_code, status, path)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(len(soup.select('main')), 1, path)
        self.assertEqual(len(soup.select('h1')), 1, path)
        self.assertTrue(soup.select_one('link[rel="canonical"]'), path)
        for schema in soup.select('script[type="application/ld+json"]'):
            json.loads(schema.string)
        for asset in soup.select('img[src], script[src], link[rel="stylesheet"]'):
            url = asset.get('src') or asset.get('href')
            if url.startswith('/static/'):
                with self.client.get(url) as asset_response:
                    self.assertEqual(asset_response.status_code, 200, url)
        return soup

    def test_empty_pages_and_error_states(self):
        home = self.page('/')
        self.assertFalse(home.select('.testimonial-card'))
        self.assertTrue(home.select_one('.belief-block'))
        self.assertTrue(self.page('/blog').select_one('.empty-block'))
        self.assertTrue(self.page('/eventos').select_one('.empty-block'))
        self.page('/casamento-em-crise')
        self.page('/pagina-inexistente', 404)
        with self.app.test_request_context('/'):
            soup = BeautifulSoup(render_template('errors/500.html'), 'html.parser')
            self.assertEqual(len(soup.select('main')), 1)
            self.assertEqual(len(soup.select('h1')), 1)

    def test_content_visibility_and_pagination(self):
        with self.app.app_context():
            seed_content()
        home = self.page('/')
        self.assertEqual(len(home.select('.testimonial-card')), 1)
        self.assertNotIn('Depoimento oculto.', home.get_text())
        blog = self.page('/blog')
        self.assertEqual(len(blog.select('.blog-card')), 9)
        self.assertTrue(blog.select_one('.pagination-nav a[rel="next"]'))
        self.assertEqual(len(self.page('/blog?page=2').select('.blog-card')), 1)
        self.assertNotIn('Rascunho privado', blog.get_text())
        self.page('/blog/rascunho-privado', 404)
        self.assertTrue(self.page('/blog/reflexao-0').select_one('.article-content h2'))
        events = self.page('/eventos')
        self.assertEqual(len(events.select('.event-card')), 10)
        self.assertEqual(len(self.page('/eventos?page=2').select('.event-card')), 1)
        self.assertNotIn('Evento inativo', events.get_text())
        self.assertIn('OUT 2026', events.select_one('.event-card__date').get_text())

    def test_home_anchors_and_schema_selectors_resolve(self):
        for path in ['/', '/casamento-em-crise']:
            soup = self.page(path)
            for anchor in soup.select('a[href^="#"]'):
                self.assertIsNotNone(soup.find(id=anchor['href'][1:]), anchor['href'])
            for schema in soup.select('script[type="application/ld+json"]'):
                data = json.loads(schema.string)
                for selector in data.get('speakable', {}).get('cssSelector', []):
                    self.assertTrue(soup.select(selector), selector)
        self.assertTrue(soup.select_one('dialog[aria-labelledby]'))

    def test_admin_styles_remain_separate(self):
        with self.app.app_context():
            seed_content()
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertTrue(soup.select_one('.login-card input[autocomplete="current-password"]'))
        token = soup.select_one('input[name="csrf_token"]')['value']
        logged_in = self.client.post('/admin/login', data={
            'username': 'Equipe de teste', 'password': 'Frontend-test-only-123!',
            'csrf_token': token,
        })
        self.assertEqual(logged_in.status_code, 302)
        dashboard = self.client.get('/admin/')
        self.assertEqual(dashboard.status_code, 200)
        self.assertIn(b'css/style.css', dashboard.data)
        self.assertNotIn(b'css/public.css', dashboard.data)


if __name__ == '__main__':
    unittest.main()
