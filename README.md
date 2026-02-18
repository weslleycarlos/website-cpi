# 💒 Casamento Plano Infalível (CPI)

Website oficial do projeto **Casamento Plano Infalível** - Mentoria cristã para casais focada em fortalecer relacionamentos conjugais através de princípios bíblicos.

## 🚀 Tecnologias

- **Backend:** Flask 3.1.2 (Python)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **ORM:** SQLAlchemy 2.0 + Flask-Migrate
- **Auth:** Flask-Login + bcrypt
- **Security:** Flask-Talisman (CSP, HTTPS)
- **Frontend:** HTML5, CSS3 (layout moderno mobile-first), Vanilla JavaScript
- **Deploy:** Railway + Gunicorn

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Git

## ⚙️ Configuração Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/website-cpi.git
cd website-cpi
```

### 2. Crie e ative o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
copy .env.example .env   # Windows
# ou
cp .env.example .env     # Linux/Mac
```

**Edite o arquivo `.env`** e configure:

```dotenv
# Gere uma SECRET_KEY segura
SECRET_KEY=sua-chave-super-secreta-aqui

# Defina senha forte para o admin
ADMIN_PASSWORD=SuaSenhaForte123!

# Email do admin (opcional)
ADMIN_EMAIL=seu-email@exemplo.com

# Ambiente
FLASK_ENV=development
```

**💡 Dica:** Gere uma SECRET_KEY segura com:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Inicialize o banco de dados

```bash
# Criar banco de dados e usuário admin
flask seed-db
```

Este comando:
- ✅ Cria as tabelas do banco de dados
- ✅ Cria o usuário admin com a senha do `.env`
- ✅ Adiciona dados de exemplo (posts, depoimentos, eventos)

### 6. Execute o servidor de desenvolvimento

```bash
python run.py
```

O site estará disponível em: **http://localhost:5000**

**Admin Panel:** http://localhost:5000/admin/login

- **Usuário:** admin
- **Senha:** (a que você definiu em `ADMIN_PASSWORD`)

## 🗄️ Comandos Úteis

```bash
# Criar novas migrações (após alterar models.py)
flask db migrate -m "Descrição da mudança"

# Aplicar migrações
flask db upgrade

# Reverter última migração
flask db downgrade

# Resetar banco de dados (⚠️ APAGA TUDO)
flask seed-db

# Verificar rotas disponíveis
flask routes

# Abrir shell interativo com contexto da aplicação
flask shell
```

## 🚀 Deploy em Produção (Railway)

### 1. Pré-requisitos

- Conta no [Railway](https://railway.app/)
- Repositório Git (GitHub, GitLab, etc.)
- Código commitado no repositório

### 2. Configuração no Railway

1. **Crie novo projeto:**
   - Acesse https://railway.app/
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha o repositório `website-cpi`

2. **Adicione PostgreSQL:**
   - Clique em "+ New"
   - Selecione "Database" → "PostgreSQL"
   - Railway criará automaticamente a variável `DATABASE_URL`

3. **Configure variáveis de ambiente:**
   
   Vá em **Variables** e adicione:

   ```
   SECRET_KEY=<gere-uma-chave-segura-64-caracteres>
   ADMIN_PASSWORD=<senha-forte-para-admin>
   ADMIN_EMAIL=seu-email@exemplo.com
   FLASK_ENV=production
   ```

   **⚠️ Importante:** Não use as mesmas credenciais de desenvolvimento!

4. **Deploy automático:**
   - Railway detecta automaticamente o `Procfile`
   - O build inicia automaticamente
   - Aguarde a conclusão (2-5 minutos)

### 3. Inicialização do Banco de Dados (primeira vez)

Após o primeiro deploy, execute **uma única vez**:

```bash
# No terminal do Railway (ou via CLI)
python setup_railway.py
```

Este script:
- ✅ Cria todas as tabelas no PostgreSQL
- ✅ Cria o usuário admin
- ✅ **Não** cria dados de exemplo (apenas produção limpa)

### 4. Acessar o site

Seu site estará disponível em:
```
https://seu-projeto.up.railway.app
```

**Admin:** `https://seu-projeto.up.railway.app/admin/login`

### 5. Deploy de atualizações

```bash
# Faça suas alterações
git add .
git commit -m "Descrição das alterações"
git push origin main
```

Railway detecta o push e faz deploy automático! 🚀

## 🏗️ Estrutura do Projeto

```
website-cpi/
├── app/
│   ├── __init__.py          # Factory pattern + config
│   ├── models.py            # Models SQLAlchemy
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas admin (autenticadas)
│   ├── static/
│   │   ├── css/style.css
│   │   ├── css/public.css      # Novo design público (home/blog/eventos/crise)
│   │   ├── js/script.js
│   │   └── images/
│   └── templates/
│       ├── base.html        # Template base público
│       ├── index.html
│       ├── blog_list.html
│       └── admin/           # Templates admin
├── migrations/              # Versionamento de DB
├── .env.example            # Template de variáveis
├── requirements.txt        # Dependências Python
├── run.py                  # Entry point
├── Procfile               # Config Railway/Gunicorn
└── railway.json           # Config Railway

```

## 🔐 Segurança

### Recursos Implementados

- ✅ **CSP (Content Security Policy)** via Flask-Talisman
- ✅ **HTTPS** forçado em produção
- ✅ **CSRF Protection** com Flask-WTF
- ✅ **Password Hashing** com bcrypt
- ✅ **SQL Injection Protection** via SQLAlchemy ORM
- ✅ **XSS Protection** com HTML sanitization (Bleach)
- ✅ **Secure Cookies** em produção
- ✅ **Environment-based secrets** (sem hardcode)

### Boas Práticas

1. **Nunca commite o arquivo `.env`** (já está no `.gitignore`)
2. **Use senhas fortes** (min. 8 caracteres, maiúscula, minúscula, número)
3. **SECRET_KEY diferente** para dev e production
4. **Atualize dependências** regularmente: `pip list --outdated`

## 📱 UX/UI Mobile-First

O site foi otimizado para dispositivos móveis com:

- ✅ Touch targets >= 44px (Apple HIG)
- ✅ Contraste WCAG AA
- ✅ ARIA labels e roles
- ✅ Focus states acessíveis
- ✅ Safe area insets (iPhone notch)
- ✅ Responsive design (320px+)
- ✅ Menu mobile com overlay

### Frontend público (refatorado)

- `app/templates/base.html`: header moderno fixo + navegação desktop/mobile
- `app/templates/index.html`: landing page em seções com hierarquia de conversão
- `app/templates/blog_list.html`, `blog_post.html`, `eventos.html`, `casamento_crise.html`: páginas públicas no mesmo design system
- `app/static/css/public.css`: estilos exclusivos do frontend público (sem impactar admin)
- `app/static/js/script.js`: interações leves (menu mobile, transições de seção, contadores, ajuste de âncoras)

## 🐛 Troubleshooting

### Erro: "The CSRF token is missing"

**Solução:** Todos os formulários já têm o token CSRF. Se ainda aparecer:
1. Limpe o cache do navegador (Ctrl+Shift+Del)
2. Reinicie o servidor Flask
3. Verifique se o arquivo `.env` tem `SECRET_KEY` configurado

### Erro: "SECRET_KEY must be set in production"

**Solução:** Configure a variável `SECRET_KEY` no Railway ou `.env`

### Erro: "no such table: usuario"

**Solução:** Execute `flask seed-db` (local) ou `python setup_railway.py` (Railway)

### Erro: "Address already in use"

**Solução:** Porta 5000 ocupada. Mate o processo ou defina outra porta antes de iniciar:
```bash
# Linux/Mac
PORT=5001 python run.py

# Windows PowerShell
$env:PORT=5001; python run.py
```

### Erro: "ModuleNotFoundError"

**Solução:** Reinstale as dependências:
```bash
pip install -r requirements.txt
```

### Erro de migração no Railway

**Solução:** 
```bash
# Via Railway CLI
railway run flask db upgrade
```

## 📄 Licença

© 2025 Casamento Plano Infalível. Todos os direitos reservados.

## 👥 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📞 Contato

- **Instagram:** [@cpi_casamentoplanoinfalivel](https://www.instagram.com/cpi_casamentoplanoinfalivel)
- **YouTube:** [@C.P.I.casamento](https://www.youtube.com/@C.P.I.casamento)
- **WhatsApp:** +55 61 99803-9461

---

**Feito com ❤️ para fortalecer casamentos**