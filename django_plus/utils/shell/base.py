import abc
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from django_plus.utils.shell.runners import AbstractShell, IPython, Plain, ShellContext
from django_plus.utils.shell.typings import TypeDirectiveTuple, TypeShellRunner

PREFERRED_RUNNERS = [
    'ptipython',
    'ptpython',
    'bpython',
    'ipython',
    'plain'
]


@contextmanager
def cursor_wrapper(**kwargs: Any):
    yield


class AbstractShellBuilder(abc.ABC):
    def __init__(self):
        self._shell_context: ShellContext = ShellContext()

    @property
    @abc.abstractmethod
    def shell(self) -> TypeShellRunner:
        pass

    @abc.abstractmethod
    def set_application_name(self, options: dict[str, Any]):
        pass

    @abc.abstractmethod
    def load_runner(self, runner_name: str, options: dict[str, Any]):
        """Based on the runner name, load the appropriate 
        shell runner (e.g. IPython, PTpython, etc.)
        
        Args:
            runner_name (str): The name of the runner to load.
        """
        self._runner_name = runner_name

    @abc.abstractmethod
    def import_models(self):
        """Load all the models into the shell context. This allows
        the user to access the models directly in the shell without
        having to import them manually.
        """

    @abc.abstractmethod
    def import_directives(self):
        """Import any additional directives or commands into the shell context.
        This can include custom commands, utilities, or any otherwise useful functions 
        that should be available in the shell environment.
        """

    @abc.abstractmethod
    def import_subclasses(self):
        """Import any subclasses of the models into the shell context. This allows
        the user to access the subclasses directly in the shell without having to 
        import them manually.
        """


class ShellBuilder(AbstractShellBuilder):
    """A builder class that constructs the shell based on the 
    provided runner name and options. It also loads all the required
    elements (e.g. models) into the shell context. The builder can be
    swapped out for a different implementation if needed, as long as it
    adheres to the AbstractShellBuilder interface.
    """
    def __init__(self):
        super().__init__()

        self._runner_name: str | None = None
        self._shell_instance: AbstractShell | None = None

        self._runners: dict[str, type[AbstractShell]] = {
            'ipython': IPython,
            'plain': Plain,
        }

        self.omit: list[str] = getattr(settings, "DJANGO_PLUS_SHELL_PLUS_OMIT", [])
        self.initial_imports: list[str] = getattr(settings, "DJANGO_PLUS_SHELL_PLUS_INITIAL_IMPORTS", [])
        
    @property
    def shell(self):
        """Return the underlying runner for the shell. If no runner 
        is specified, it defaults to the Plain shell."""
        if self._runner_name is None:
            self._runner_name = 'plain'

        if self._shell_instance is None:
            klass = self._runners.get(self._runner_name, Plain)
            self._shell_instance = klass()
        return self._shell_instance(context=self._shell_context)

    def _get_runner_by_flag(self, runner_flag: str) -> Callable | None:
        pass

    def _try_runner(self, runner: Callable):
        pass

    def _load_apps_and_models(self):
        """Load all the apps and their models."""
        for app in apps.get_app_configs():
            if app.models_module is not None:
                yield app.models_module, app.get_models()

    def load_runner(self, runner_name, options):
        super().load_runner(runner_name, options)

        if runner_name is not None:
            pass

    def import_models(self):
        models = self._load_apps_and_models()

        for mod, model_list in models:
            self._shell_context[mod.__name__] = mod
            for model in sorted(model_list, key=lambda m: m._meta.model_name):
                self._shell_context[model._meta.model_name] = model

    def import_directives(self) -> TypeDirectiveTuple:
        for directive in self.initial_imports:
            pass

    def import_subclasses(self):
        pass

    def set_application_name(self, options: dict[str, Any]):
        pass


class ShellCreator:
    """A class that creates a given shell based on the provided options.
    It uses the ShellBuilder to construct the shell and load the
    appropriate runner and models.

    Attributes:
        command (BaseCommand): The management command that is invoking the shell.
        options (dict[str, Any]): A dictionary of options passed to the command.
        builder (AbstractShellBuilder): The builder that constructs the shell.
        runner_name (str | None): The name of the runner to use for the shell.
        runner (AbstractShell | None): The runner instance that will be used to run the shell
        shell_settings (dict[str, Any]): A dictionary of settings for the shell.
        omit (list[str]): A list of models or apps to omit from the shell context.
        initial_imports (list[str]): A list of initial imports to include in the shell context
    """

    def __init__(self, command: BaseCommand, options: dict[str, Any]):
        self._builder: AbstractShellBuilder = None
        self.options = options
        # Represents the runner instance, e.g. IPython, PTpython, etc.
        # that will be used to run the shell. This is set by the builder 
        # when loading the runner.
        self.runner_name: str | None = options.get('runner', None)
        self.runner = None
        self.command = command
        self.shell_settings: dict[str, Any] = getattr(settings, "DJANGO_PLUS_SHELL_PLUS", {})

    @property
    def builder(self) -> AbstractShellBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: AbstractShellBuilder) -> None:
        self._builder = builder

    def get_minimal_shell(self):
        pass

    def get_shell(self):
        with cursor_wrapper():
            self.builder.set_application_name(self.options)
            self.builder.load_runner(self.runner_name, self.options)

            self.builder.import_directives()
            self.builder.import_models()
            self.builder.import_subclasses()

            return self.builder.shell


def create_shell(command: BaseCommand, options: dict[str, Any]):
    """A utility function that creates and runs a shell based on the provided
    command and options. It uses the ShellCreator to construct the shell and
    load the appropriate runner and models. This function is typically called
    from the handle method of a management command.
    
    Args:
        command (BaseCommand): The management command that is invoking the shell.
        options (dict[str, Any]): A dictionary of options passed to the command.
    """
    creator = ShellCreator(command, options)
    creator.builder = ShellBuilder()
    runner = creator.get_shell()
    runner()
