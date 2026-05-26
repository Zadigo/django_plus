---
applyTo: "django_plus/**/*.py"
description: "Django plus enhances Django applications with additional features and utilities. It provides a set of tools and libraries to simplify common tasks in Django development, such as authentication, permissions, and API development."
---

# Django Backend Instructions

**context**

- The core applicatins of Django Plus are:
    - `django_plus/db`: Provides database utilities and extensions for Django models, including custom fields, querysets, and managers.
    - `django_plus/auth`: Offers authentication and authorization features, such as custom user models, authentication backends, and permission handling.

<!-- - The backend is an ASGI Django app with `daphne`, `channels`, `graphene_django`, `drf-spectacular`, Celery, Redis, and RabbitMQ configured in [blindest/blindtest/settings.py](blindest/blindtest/settings.py).
- Core product apps are `songs`, `games` and `tvshows`. Changes in those apps often span models, `api/`, `graphql/`, `tasks.py`, `routing.py`, `consumers.py`, and tests.
- Keep REST endpoints under `/v1/` consistent with GraphQL behavior. If you change a model or business rule, inspect both surfaces before stopping.
- Websocket behavior is part of the product architecture. Read [blindest/blindtest/asgi.py](blindest/blindtest/asgi.py) and the app `routing.py` files before changing consumers or auth flow.
- Test discovery is configured in [blindest/pytest.toml](blindest/pytest.toml) and coverage settings live in [blindest/pyproject.toml](blindest/pyproject.toml).
- Use `cd blindest && pytest` as the default validation command. Narrow to affected tests when you can.
- Keep settings and env-sensitive changes minimal. The checked-in settings default to SQLite for local DB state, but Channels and Celery still depend on Redis and RabbitMQ settings.
- Files for deployment can be found in the root [docker-compose.yaml](docker-compose.yaml) and [blindest/Dockerfile](blindest/Dockerfile). Use those as references for env vars, mounted paths, and port configuration when relevant.
 -->
