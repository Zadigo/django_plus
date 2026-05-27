# Django Plus ➕

Django Plus is a collection of utilities and extensions for Django, designed to enhance the development experience and provide additional functionality. It includes features such as enhanced model fields, custom management commands, and improved testing utilities.

## Using Django Plus ⚡️

You can install Django Plus using `uv` (Universal Virtualenv) by running the following commands:

```bash
uv init
uv add django-plus
```

### Enabling Django Plus 

To enable Django Plus in your Django project, add it to your `INSTALLED_APPS` in the `settings.py` file:

```python
INSTALLED_APPS = [
    ...
    'django_plus',
    ...
]
```

### Using the commands

Django Plus provides several custom management commands that can be used to enhance your development workflow. To see a list of available commands, run:

```bash
python manage.py help
```

For example, to use `clean_pyc` command to remove all `.pyc` files from your project, run:

```bash
python manage.py clean_pyc
```

## Contributing ✍🏽

Contributions to Django Plus are welcome! If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request on the GitHub repository.
