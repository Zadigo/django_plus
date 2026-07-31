# AGENTS.md

## Scope

These instructions apply to the whole workspace. Use them with the path-scoped files in `.github/instructions/`.

## Repository Shape

- `django_plus` folder contains the core Django Plus commands and utilities.

  - The [management/commands](django_plus/management/commands) directory contains custom Django management commands, such as `load_users.py`, which is used to load users from a specified file including:
    - `check_media_root` to ensure the media root directory is properly configured.
    - `clean_pyc` to remove compiled Python files.
    - `clear_cache` to clear the cache.
    - `export_emails` to export user emails to a file.
    - `find_template` to locate a specific template.
    - `generate_password` to generate a random password.
    - `list_signals` to list all registered signals.
    - `load_users` to load users from a specified file.
    - `print_settings` to print the current Django settings.
    - `shell_plus` to start an enhanced Django shell.
    - `show_urls` to display all URL patterns in the project.
    - `sync_s3` to synchronize files with an S3 bucket.
- The main application for testing is `tests.testapp` ([source](tests/testapp)), which includes a variety of models and configurations to test different aspects of Django Plus.
- The `manage.py` file is configured to use the settings from `tests.testapp.settings` ([source](tests/testapp/settings.py)).

## First References

- Start with [README.md](README.md) for the product overview and high-level architecture.

## Working Commands

- Build project: `uv build`
- Update version
  - `uv version --bump patch`
  - `uv version --bump major`
  - `uv version --bump minor`
  - `uv version --bump minor --bump dev=1 --dry-run`

## Repo Conventions

## Validation Strategy

- Prefer focused validation from the touched area before running broad suites.
- For backend-only changes, run `pytest` from `django_plus/`.
- For frontend-only changes, run the narrowest matching script from `mainsite/package.json`.
