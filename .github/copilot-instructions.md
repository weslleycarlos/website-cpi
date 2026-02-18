# Copilot Instructions - Casamento Plano Infalível Website

## Project Overview
Flask-based website for "Casamento Plano Infalível" (CPI), a Christian couples mentoring service. The site features a public-facing blog/event showcase and an admin panel for content management. Deployed on Railway with PostgreSQL in production, SQLite for local development.

## Architecture & Key Components

### Application Structure
- **Factory Pattern**: App initialization via `create_app()` in [app/__init__.py](app/__init__.py)
- **Blueprint Separation**: 
  - `main_bp` ([app/routes.py](app/routes.py)) - Public routes (homepage, blog, events, SEO pages)
  - `admin_bp` ([app/admin_routes.py](app/admin_routes.py)) - Admin panel at `/admin/*` with authentication
- **Security**: Flask-Talisman enforces CSP, HTTPS in production, secure cookies
- **Database**: SQLAlchemy with Flask-Migrate for migrations; automatic SQLite fallback

### Data Models ([app/models.py](app/models.py))
- **Usuario**: Admin users with bcrypt password hashing via `set_password()/check_password()`
- **Post**: Blog posts with `slug` (unique URL), `is_published` flag, author relationship
- **Depoimento**: Testimonials with `is_visible` toggle
- **Evento**: Events with `is_active` flag and `event_date` for sorting

### Template Architecture
- **Public**: [app/templates/base.html](app/templates/base.html) - sidebar nav, mobile hamburger menu, SEO meta tags, Google Analytics
- **Admin**: Separate [app/templates/admin/base.html](app/templates/admin/base.html) with breadcrumb navigation ([app/templates/admin/includes/breadcrumb.html](app/templates/admin/includes/breadcrumb.html))
- **Static**: CSS/JS in [app/static/](app/static/), robots.txt served from static folder

## Development Workflow

### First-Time Setup
```powershell
# Copy environment template
Copy-Item .env.example .env

# Generate secure SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
# Add to .env manually

# Set ADMIN_PASSWORD in .env

# Run app (auto-creates SQLite database)
python run.py
```

### Database Management
- **Migrations**: Use Flask-Migrate via CLI: `flask db migrate -m "description"` then `flask db upgrade`
- **Seeding (dev only)**: `flask seed-db` creates admin user from `ADMIN_PASSWORD` env var
- **Production Setup**: [setup_railway.py](setup_railway.py) handles Railway initial database setup

### Running the Application
- **Development**: `python run.py` (auto-creates tables if not exists)
- **Production**: Gunicorn via [Procfile](Procfile): `gunicorn run:app --bind 0.0.0.0:$PORT`

## Project-Specific Conventions

### Security-First Approach
- **NEVER hardcode credentials**: All secrets via environment variables (see [.env.example](.env.example))
- **Environment-aware security**: CSP, HTTPS, secure cookies enforced only in `FLASK_ENV=production`
- **Password handling**: Always use `Usuario.set_password()` and `check_password()`, never raw hashes

### Content Management Patterns
- **Visibility Toggles**: All admin-managed content uses boolean flags (`is_published`, `is_visible`, `is_active`)
- **Slugs for URLs**: Blog posts use unique `slug` field, not IDs: `/blog/<slug>` pattern
- **Author Tracking**: Posts have `author_id` FK to Usuario (use `current_user.id` when creating)

### Database URL Handling
Special Railway compatibility in [app/__init__.py](app/__init__.py):
```python
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

### SEO & Public Pages
- **Hardcoded sitemap**: [app/routes.py](app/routes.py) returns XML string (no dynamic generation)
- **Dedicated landing pages**: `/casamento-em-crise` route for targeted content
- **Schema.org markup**: JSON-LD in [app/templates/base.html](app/templates/base.html)

## Common Tasks

### Adding New Admin Features
1. Add route to [app/admin_routes.py](app/admin_routes.py) with `@login_required` decorator
2. Create template in [app/templates/admin/](app/templates/admin/)
3. Update breadcrumb in [app/templates/admin/includes/breadcrumb.html](app/templates/admin/includes/breadcrumb.html)
4. Link from [app/templates/admin/dashboard.html](app/templates/admin/dashboard.html)

### Database Schema Changes
1. Modify model in [app/models.py](app/models.py)
2. Generate migration: `flask db migrate -m "Add field to Model"`
3. Review migration file in `migrations/versions/`
4. Apply: `flask db upgrade`
5. Test in Railway staging before production deploy

### Deployment (Railway)
- **Auto-deploy**: Git push triggers build via [railway.json](railway.json)
- **Environment Variables Required**: `SECRET_KEY`, `ADMIN_PASSWORD`, `DATABASE_URL` (auto-provided), `FLASK_ENV=production`
- **First Deploy**: Run `python setup_railway.py` once to initialize database and admin user

## Important Files Reference
- [run.py](run.py) - Application entry point, CLI commands
- [requirements.txt](requirements.txt) - Python dependencies (Flask 3.x, SQLAlchemy 2.x)
- [Procfile](Procfile) - Gunicorn config for production
- [railway.json](railway.json) - Railway deployment configuration
