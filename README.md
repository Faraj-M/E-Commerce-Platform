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

<!--

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
-->



## Project Notes

- **API design & external integration** – Django REST Framework viewsets in `apps.catalog`, `apps.orders`, `apps.accounts`, and `apps.payments` expose CRUD endpoints documented in `docs/API.md`; the payments module creates Stripe PaymentIntents and listens for webhooks in `apps/payments/views.py`.
- **Architecture & separation** – Monolithic Django MTV split into modular apps plus shared `core` utilities, server-rendered templates in `frontend/templates`, and DRF routers mounted under `/api`; PlantUML diagrams in `docs/architecture/*.puml` describe the running stack (PostgreSQL, Redis, Stripe).
- **Authentication & security** – Custom `accounts.User` model with Django session auth + allauth backend, login/signup/profile flows in `apps/accounts/views.py`, `login_required` around checkout and payments, staff-only filtering inside API viewsets, CSRF defaults, and Stripe webhook signature checks.
- **Database & ORM** – PostgreSQL schema managed through Django migrations (`apps/*/migrations/0001_initial.py`) with relationships tying `User`, `Product`, `Order`, `OrderItem`, and `Payment`; catalog fixtures (`apps/catalog/fixtures/sample_data.json`) seed demo data during Docker boot.
- **Deployment & DevOps** – Dockerfile builds the Gunicorn web image, while `docker-compose.yml` orchestrates web, Postgres, and Redis, runs migrations + sample data, injects secrets from `.env`, and wires Stripe keys; `generate-secret-key.sh` assists local runs.
- **Version control & collaboration** – Shared Git repo with Docker-first onboarding documented here, architecture notes in `docs/`, and modular app folders that keep pair-programming responsibilities easy to split.
- **Code quality & documentation** – Central helpers live in `backend/common`, serializers/models carry docstrings, API reference is tracked in `docs/API.md`, and PlantUML diagrams plus architecture notes make the design review-ready; HTMX/Tailwind placeholders under `frontend/static` mark where presentation polish lands.

### Still to implement
- **Testing & QA** – `backend/tests/` only has a placeholder; unit, API, and Selenium coverage still need to be written.
- **Performance optimization** – No PageSpeed runs, caching strategy, or Tailwind build yet (`frontend/static/css/main.css` is still a stub).
- **CI/CD & ops polish** – No automated pipeline, HTTPS termination, Celery worker container, or Stripe webhook tunnel automation; deployment docs still assume manual `docker-compose up`.
