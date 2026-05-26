from django_plus.management.signals import post_command, pre_command
from typing import Any
from typing import Callable


def signalcommand(func: Callable) -> Callable:
    """Decorator used for management commands to send signals 
    before and after a given command is executed."""

    def inner(self, *args, **kwargs) -> Any:
        pre_command.send(self.__class__, args=args, kwargs=kwargs)

        try:
            result = func(self, *args, **kwargs)
        except Exception as e:
            post_command.send(
                self.__class__,
                args=args,
                kwargs=kwargs,
                outcome=e
            )
            raise
        else:
            post_command.send(
                self.__class__,
                args=args,
                kwargs=kwargs,
                outcome=result
            )
        return result

    return inner
