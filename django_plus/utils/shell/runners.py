import abc
import sys
import traceback
from types import ModuleType
from typing import Any

from django.db.models import Model

from django_plus.utils.shell.typings import TypeShellRunner


class ShellContext(dict[str, Model | ModuleType | Any]):
    """A dictionary-like object that holds the context for the shell. 
    It can be used to store variables and other information that should
    be available in the shell environment such as models, settings, etc. 
    It is passed to the shell runner when it is invoked.
    """


def shell_runner(flags: list[str], name: str, help: str | None = None):
    def decorator(klass: type[AbstractShell]):
        klass.runner_flags = flags
        klass.runner_name = name
        klass.runner_help = help

        return klass

    return decorator


class AbstractShell(abc.ABC):
    def __init__(self):
        self.flags: list[str] = []
        self.name: str = ""
        self.help: str | None = None

    @abc.abstractmethod
    def __call__(self, *args, **kwargs: ShellContext | Any) -> TypeShellRunner:
        pass


@shell_runner(flags=[], name="kernel", help="Start a Jupyter kernel")
class Kernel(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="notebook", help="Start a Jupyter notebook")
class Notebook(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="jupyterlab", help="Start JupyterLab")
class JupyterLab(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="plain", help="Standard Python shell")
class Plain(AbstractShell):
    """This shell uses the standard Python shell. It is 
    the default shell if no other shell is specified."""
    
    def __call__(self, *args, **kwargs: ShellContext | Any):
        shell_context = kwargs.get('context', ShellContext())

        use_python_rc = shell_context.get('use_python_rc', True)
        startup = shell_context.get('startup', False)

        if use_python_rc or not startup:
            pass

        try:
            hook = sys.__interactivehook__
        except AttributeError:
            hook = None

        if hook is not None:
            try:
                hook()
            except Exception:
                traceback.print_exc()

        try:
            # Import readline to enable command history and 
            # line editing in the standard Python shell.
            import readline
        except ImportError:
            pass
        else:
            # No need to wrap the following import in a 'try', because
            # we already know 'readline' was imported successfully.
            import rlcompleter

            readline.set_completer(rlcompleter.Completer(shell_context).complete)   
            # Enable tab completion on systems using libedit (e.g. macOS).
            # These lines are copied from Lib/site.py on Python 3.4.
            readline_doc = getattr(readline, "__doc__", "")
            if readline_doc is not None and "libedit" in readline_doc:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

        # import code
        # return lambda: code.interact(local=shell_context)
        return lambda: print('Hourrah! You are in the standard Python shell. Type "exit()" to exit.')
        

@shell_runner(flags=[], name="bpython", help="Start a bpython shell")
class BPython(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="ipython", help="Start an IPython shell")
class IPython(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="ptpython", help="Start a PTpython shell")
class PTpython(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="ptipython", help="Start a PTIPython shell")
class PTIPython(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


@shell_runner(flags=[], name="idle", help="Start an IDLE shell")
class Idle(AbstractShell):
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass
