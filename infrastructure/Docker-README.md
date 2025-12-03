# Infrastructure

This directory contains deployment and DevOps configuration files.

## Files

- **Dockerfile** - Builds the Django application container image
- **docker-compose.yml** - Orchestrates the multi-container setup (web, database, redis)

## Usage

Run Docker Compose from this directory or from the project root:

```bash
# From infrastructure directory
docker-compose up --build

# From project root
docker-compose -f infrastructure/docker-compose.yml up --build
```

## Future Additions

This directory will also contain:
- CI/CD pipeline configurations (GitHub Actions, GitLab CI, etc.)
- Kubernetes manifests (if needed)
- Deployment scripts
- Monitoring and logging configurations

