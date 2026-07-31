from django.core.checks import Tags, register


class DjangoPlusTags(Tags):
    shell = "shell"


@register(DjangoPlusTags.shell)
def check_shell_plus_settings(app_configs, **kwargs):
    print(app_configs)
    return []
