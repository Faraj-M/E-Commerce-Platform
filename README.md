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

