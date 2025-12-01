# E-Commerce Platform

## Quick Start with Docker

### Prerequisites
- Docker installed: You can download it from the official Docker website -> https://www.docker.com/.
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Faraj-M/E-Commerce-Platform.git
   cd E-Commerce-Platform
   ```

2. **Configure Stripe keys (optional)**:
   - A `.env` file with safe defaults is already included. The app will run without changes, but payment flows need real Stripe test keys.
   - To use payments, edit `.env` and replace the placeholder values for `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` with keys from https://dashboard.stripe.com/test/apikeys.
   - `DJANGO_SECRET_KEY` can stay blank—Docker auto-generates it on boot.

3. **Build and run with Docker** (Docker Desktop must be running):
   ```bash
   docker-compose up --build
   ```

4. **Create admin user** (run after the containers start):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Sample Data

Sample products are automatically loaded when the container starts. You can also load them manually:
```bash
docker-compose exec web python manage.py loaddata sample_data
```

### Managing Database Changes
- If you modify models, regenerate migrations inside Docker:
  ```bash
  docker-compose run --rm web python manage.py makemigrations
  docker-compose run --rm web python manage.py migrate
  ```
- To reapply fixtures or reset data, run `docker-compose exec web python manage.py loaddata sample_data`.

### Troubleshooting
- Make sure Docker Desktop is running before `docker-compose up`.
- Check logs if something fails: `docker-compose logs -f web`.
- If you change environment values, restart the stack: `docker-compose down && docker-compose up --build`.

## Project Notes

This repo holds the planning skeleton for our Django-based e‑commerce platform. Nothing is wired up yet—these notes are just to keep both of us aligned while we start implementing.

- **Architecture**: Monolithic Django MVC/MTV with modular apps (`accounts`, `catalog`, `orders`, `payments`, `core`). Server-rendered pages with Django templates + HTMX interactivity and Tailwind styling. REST hooks later via Django REST Framework.
- **Data + Infra**: PostgreSQL primary DB, Redis for caching/background jobs (Celery or RQ). Stripe handles payments + webhooks. Docker compose will orchestrate web, worker, db, redis (to be added under `infrastructure/`).
- **Dev stack**: Python 3.12+, Poetry for dependency/virtualenv management, Node 20+ for Tailwind build, GitHub repo already linked. Keep commits frequent and descriptive.

### Codespace Notes
1. Install PlantUML extention for VS Code to view the UML diagram (i'll make a nicer one after the project is done its just easier to edit it this way for both of us) 
2. Install Poetry: https://python-poetry.org/docs/. 
    - after we add dependencies; inside this folder run `poetry install` and `poetry shell` for a virtual env.  
3. Node/Tailwind: install Node 20+, then `npm install` once we add the frontend package manifest.  
4. Copy `.env.example` (once we add it) to `.env` with Django secret, DB creds, Stripe keys, etc.

### File Structure
- `backend/`
  - `ecommerce_platform/`: project config (settings, urls, ASGI/WSGI).  
  - `apps/`: feature modules (`accounts`, `catalog`, `orders`, `payments`, `core`) with stubs for models, views, serializers, services, tests.  
  - `common/`: shared utilities/exceptions.  
  - `tests/`: top-level pytest fixtures and smoke tests.
- `frontend/`
  - `templates/`: Django base templates; HTMX partials will live here.  
  - `static/css/main.css`: Tailwind build output placeholder.  
  - `static/js/app.js`: HTMX/Tailwind helper scripts placeholder.  
  - `static/img/placeholder.txt`: marker for design assets.
- `docs/architecture/`
  - `diagram-notes.md`: running log of UML tasks.  
  - `high-level-overview.puml`: PlantUML component diagram for the monolith.
- `infrastructure/notes.txt`: reminder that Docker/CI assets will land here.
- `requirements.txt`: mirrors Poetry dependencies for reference/CI.
