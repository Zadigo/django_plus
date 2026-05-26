# AGENTS.md

## Scope

These instructions apply to the whole workspace. Use them with the path-scoped files in `.github/instructions/`.

## Repository Shape

- `django_plus` contains the core Django Plus applications and utilities.
- The main application for testing is `tests.testapp` ([source](tests/testapp)), which includes a variety of models and configurations to test different aspects of Django Plus.
- The `manage.py` file is configured to use the settings from `tests.testapp.settings` ([source](tests/testapp/settings.py)).

## First References

- Start with [README.md](README.md) for the product overview and high-level architecture.

## Working Commands

- Server: `python manage.py runserver`
- Tests: `python manage.py test`

## Repo Conventions

## Validation Strategy

- Prefer focused validation from the touched area before running broad suites.
- For backend-only changes, run `pytest` from `django_plus/`.
- For frontend-only changes, run the narrowest matching script from `mainsite/package.json`.
