# Casamento Plano Infalível (CPI) — Website

Site institucional do projeto **CPI**, uma mentoria cristã para casais. Construído com Flask, SQLAlchemy e Jinja2.

---

## 🛠️ Tecnologias

- **Backend:** Python 3 + Flask
- **Banco de dados:** SQLite (dev) / PostgreSQL (produção)
- **ORM:** Flask-SQLAlchemy + Flask-Migrate
- **Autenticação:** Flask-Login
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (GSAP)
- **Deploy:** Gunicorn + Railway

---

## 🚀 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/weslleycarlos/website-cpi.git
cd website-cpi
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com valores seguros:
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
ADMIN_PASSWORD=sua-senha-super-forte-aqui
```

### 5. Inicialize o banco de dados

```bash
# Cria as tabelas e popula com dados de exemplo (somente dev)
flask --app run seed-db
```

### 6. Inicie o servidor

```bash
python run.py
```

Acesse: [http://localhost:5000](http://localhost:5000)  
Admin: [http://localhost:5000/admin](http://localhost:5000/admin)

---

## 📁 Estrutura do Projeto

```
website-cpi/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── models.py            # Modelos do banco de dados
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas do painel admin
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/script.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── blog_list.html
│       ├── blog_post.html
│       ├── eventos.html
│       ├── casamento_crise.html
│       └── admin/
├── run.py                   # Ponto de entrada + CLI
├── create_admin.py          # Criar admin em produção
├── setup_admin.py           # Setup interativo de admin
├── requirements.txt
├── Procfile                 # Para deploy (Gunicorn)
├── railway.json
└── .env.example
```

---

## 🔐 Segurança

- `SECRET_KEY` **deve** ser definida via variável de ambiente — a aplicação não inicia sem ela
- Senhas armazenadas com hash (Werkzeug `generate_password_hash`)
- Rotas destrutivas (delete, toggle) protegidas com POST
- Cookies de sessão com `HttpOnly` e `Secure` em produção

---

## 🌐 Deploy em Produção

### Variáveis de ambiente obrigatórias

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta longa e aleatória |
| `ADMIN_PASSWORD` | Senha do usuário admin |
| `DATABASE_URL` | URL do PostgreSQL |
| `FLASK_ENV` | `production` |

### Criar admin em produção

```bash
python create_admin.py
```

---

## 📝 Licença

Projeto privado — todos os direitos reservados.