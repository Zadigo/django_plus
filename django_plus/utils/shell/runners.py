import abc


class AbstractShell(abc.ABC):
    pass
    # @abc.abstractmethod
    # def __call__(self, *args, **kwargs):
    #     pass


class Kernel(AbstractShell):
    pass


class Notebook(AbstractShell):
    pass


class JupyterLab(AbstractShell):
    pass


class Plain(AbstractShell):
    pass


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
