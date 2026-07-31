import abc
import sys
import traceback
from collections.abc import Callable
from typing import Any


class ShellContext(dict):
    """A dictionary-like object that holds the context for the shell. 
    It can be used to store variables and other information that should
    be available in the shell environment.
    """


def shell_runner(flags: list[str], name: str, help: str | None = None):
    def decorator(func: type[AbstractShell]):
        func.runner_flags = flags
        func.runner_name = name
        func.runner_help = help

        return func

    return decorator


class AbstractShell(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs: ShellContext | Any) -> Callable[[], None]:
        pass


class Kernel(AbstractShell):
    @shell_runner(flags=[], name="kernel", help="Start a Jupyter kernel")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class Notebook(AbstractShell):
    @shell_runner(flags=[], name="notebook", help="Start a Jupyter notebook")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class JupyterLab(AbstractShell):
    @shell_runner(flags=[], name="jupyterlab", help="Start JupyterLab")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class Plain(AbstractShell):
    """This shell uses the standard Python shell. It is 
    the default shell if no other shell is specified."""

    @shell_runner(flags=[], name="plain", help="Standard Python shell")
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

        import code
        return lambda: code.interact(local=shell_context)
        


class BPython(AbstractShell):
    @shell_runner(flags=[], name="bpython", help="Start a bpython shell")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class IPython(AbstractShell):
    @shell_runner(flags=[], name="ipython", help="Start an IPython shell")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class PTpython(AbstractShell):
    @shell_runner(flags=[], name="ptpython", help="Start a PTpython shell")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class PTIPython(AbstractShell):
    @shell_runner(flags=[], name="ptipython", help="Start a PTIPython shell")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass


class Idle(AbstractShell):
    @shell_runner(flags=[], name="idle", help="Start an IDLE shell")
    def __call__(self, *args, **kwargs: ShellContext | Any):
        pass
