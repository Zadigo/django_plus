import abc
import sys
import traceback
from collections.abc import Callable


def shell_runner(flags: list[str], name: str, help: str | None = None):
    def decorator(self, func: type[AbstractShell]):
        func.runner_flags = flags
        func.runner_name = name
        func.runner_help = help

        return func

    return decorator



class AbstractShell(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Callable[[], None]:
        pass


class Kernel(AbstractShell):
    pass


class Notebook(AbstractShell):
    pass


class JupyterLab(AbstractShell):
    pass


class Plain(AbstractShell):
    """This shell uses the standard Python shell. It is 
    the default shell if no other shell is specified."""

    @shell_runner(flags=[], name="plain", help="Standard Python shell")
    def __call__(self, *args, **kwargs):
        shell_context = kwargs.get('context', {})

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
            import rlcompleter

            readline.set_completer(rlcompleter.Completer(shell_context).complete)   
            # Enable tab completion on systems using libedit (e.g. macOS).
            # These lines are copied from Lib/site.py on Python 3.4.
            readline_doc = getattr(readline, "__doc__", "")
            if readline_doc is not None and "libedit" in readline_doc:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")


        


class BPython(AbstractShell):
    pass


class IPython(AbstractShell):
    pass


class PTpython(AbstractShell):
    pass


class PTIPython(AbstractShell):
    pass


class Idle(AbstractShell):
    pass
