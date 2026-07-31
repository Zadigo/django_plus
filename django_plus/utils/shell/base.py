import abc
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from django_plus.utils.shell.runners import AbstractShell, IPython, Plain, ShellContext

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
    @property
    @abc.abstractmethod
    def shell(self) -> AbstractShell:
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

    def load_models(self):
        pass


class ShellBuilder(AbstractShellBuilder):
    """A builder class that constructs the shell based on the 
    provided runner name and options. It also loads all the required
    elements (e.g. models) into the shell context.
    """
    def __init__(self):
        self._runner_name: str | None = None
        self._shell: AbstractShell | None = None
        self._shell_context: ShellContext = ShellContext()

        self._runners: dict[str, type[AbstractShell]] = {
            'ipython': IPython,
            'plain': Plain,
        }
        
    @property
    def shell(self):
        if self._runner_name is None:
            self._runner_name = 'plain'

        if self._shell is None:
            klass = self._runners.get(self._runner_name, Plain)()
            self._shell = klass
        return self._shell

    def _get_runner_by_flag(self, runner_flag: str) -> Callable | None:
        pass

    def _try_runner(self, runner: Callable):
        pass

    def load_runner(self, runner_name, options):
        super().load_runner(runner_name, options)

        if runner_name is not None:
            pass

    def set_application_name(self, options: dict[str, Any]):
        pass


class ShellCreator:
    """A class that creates a given shell based on the provided options.
    It uses the ShellBuilder to construct the shell and load the
    appropriate runner and models.
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

    def get_shell(self) -> AbstractShell:
        with cursor_wrapper():
            self.builder.set_application_name(self.options)
            self.builder.load_runner(self.runner_name, self.options)
            self.builder.load_models()
            return self.builder.shell


# def create_shell(command: BaseCommand, options: dict[str, Any]):
#     creator = ShellCreator(command, options)
#     creator.builder = ShellBuilder()
#     return creator.get_shell()
