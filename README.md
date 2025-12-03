# E-Commerce Platform

**MarketPlace** is a full-stack web application that allows users to browse products, manage shopping carts, and securely process payments using Stripe. Built with Django, PostgreSQL, and modern frontend technologies, it demonstrates end-to-end e-commerce functionality including user authentication, product catalogue management, order processing, and payment integration.

Demo Video: https://drive.google.com/file/d/1o7S_5AMXYrXbf27jc7EooYbtonpsLWxz/view?usp=sharing

## Quick Start with Docker

### Prerequisites
- Docker installed: You can download it from the official Docker website -> https://www.docker.com/.
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Faraj-M/E-Commerce-Platform.git
   ```

2. **Configure Stripe keys (optional for testing)**:
   - Default placeholder test keys are included in `infrastructure/docker-compose.yml` for immediate testing. The app will run, but payment flows need real Stripe test keys to work.
   - For actual payment testing, see `docs/STRIPE.md`.

3. **Build and run with Docker** (Docker Desktop must be running):
   ```bash
   cd E-Commerce-Platform
   docker-compose -f infrastructure/docker-compose.yml up --build
   ```

4. **Create admin user** (run after the containers start):
   ```bash
   docker-compose -f infrastructure/docker-compose.yml exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Running Tests

**Unit and Integration Tests**:
```bash
docker-compose -f infrastructure/docker-compose.yml exec web pytest apps/ -v
```

**End-to-End Tests** (requires application running):
```bash
# Start the application first
docker-compose -f infrastructure/docker-compose.yml up -d

# Run E2E tests
docker-compose -f infrastructure/docker-compose.yml exec web pytest tests/test_e2e.py -v
```

### Sample Data

Sample products are automatically loaded when the container starts. You can also load them manually:
```bash
docker-compose -f infrastructure/docker-compose.yml exec web python manage.py loaddata sample_data
```

## Tech Stack

### Frontend
- **HTML/CSS/JavaScript**: Server-rendered Django templates with Tailwind CSS for styling
- **HTMX**: Progressive enhancement for dynamic interactions (cart updates, form submissions)
- **Tailwind CSS**: Utility-first CSS framework loaded via CDN
- **Font Awesome**: Icon library for UI elements

### Backend
- **Python 3.12+**: Programming language
- **Django 5.0+**: Web framework (MVC/MTV pattern)
- **Django REST Framework**: RESTful API layer
- **Django Allauth**: Authentication backend
- **Gunicorn**: WSGI HTTP server for production

### Database
- **PostgreSQL 15**: Primary relational database
- **Django ORM**: Object-relational mapping for database interactions

### Infrastructure & Services
- **Docker & Docker Compose**: Containerization and orchestration
- **Redis**: Caching and session storage (future: Celery task queue)
- **Stripe API**: Payment processing integration

### Development Tools
- **Git**: Version control
- **Poetry**: Dependency management (optional, requirements.txt used for Docker)

### System Design diagrams 
- can be found under `docs/architecture`

## Project Structure

```
E-Commerce-Platform/
├── backend/                    # Django backend application
│   ├── apps/                   # Django apps (modular components)
│   │   ├── accounts/           # User authentication & profiles
│   │   │   ├── models.py       # User model (extends AbstractUser)
│   │   │   ├── views.py        # Login, signup, profile views
│   │   │   ├── urls.py         # Account routes
│   │   │   └── serializers.py  # DRF serializers for API
│   │   ├── catalog/            # Product catalog
│   │   │   ├── models.py       # Product, Category models
│   │   │   ├── views.py        # Product list/detail views
│   │   │   ├── fixtures/       # Sample product data
│   │   │   └── templatetags/   # Custom template filters
│   │   ├── orders/             # Shopping cart & orders
│   │   │   ├── models.py       # Order, OrderItem models
│   │   │   ├── views.py        # Cart, checkout, order views
│   │   │   └── urls.py         # Order routes
│   │   ├── payments/           # Payment processing
│   │   │   ├── models.py       # Payment model
│   │   │   ├── views.py        # Stripe integration, webhooks
│   │   │   └── urls.py         # Payment routes
│   │   └── core/               # Shared utilities (placeholder)
│   ├── common/                 # Common utilities
│   │   ├── utils.py           # Helper functions
│   │   └── exceptions.py      # Custom exceptions
│   ├── ecommerce_platform/    # Django project settings
│   │   ├── settings/          # Environment-specific settings
│   │   │   ├── base.py        # Base settings
│   │   │   ├── local.py       # Development settings
│   │   │   └── production.py # Production settings
│   │   ├── urls.py            # Root URL configuration
│   │   ├── wsgi.py            # WSGI application
│   │   └── asgi.py            # ASGI application
│   ├── tests/                 # Test suite (placeholder)
│   └── manage.py              # Django management script
├── frontend/                   # Frontend assets
│   ├── templates/             # Django HTML templates
│   │   ├── base.html          # Base template
│   │   ├── accounts/          # Auth templates
│   │   ├── catalog/           # Product templates
│   │   ├── orders/            # Cart & order templates
│   │   └── payments/          # Payment templates
│   └── static/                # Static files
│       ├── css/               # Stylesheets
│       ├── js/                # JavaScript files
│       └── img/               # Images
├── infrastructure/            # Deployment configuration
│   ├── Dockerfile             # Docker image definition
│   ├── docker-compose.yml     # Multi-container orchestration
│   └── README.md              # Infrastructure docs
├── docs/                      # Documentation
│   ├── API.md                 # API endpoint documentation
│   ├── STRIPE.md              # Stripe setup and testing guide
│   └── architecture/          # Architecture diagrams
│       ├── high-level-overview.png
│       ├── package-diagram.png
│       └── class-diagram.png
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```
