from collections.abc import Callable
from typing import Any

from django_plus.management.signals import post_command, pre_command


def signalcommand(func: Callable) -> Callable:
    """Decorator used for management commands to send signals 
    before and after a given command is executed.
    
    Args:
        func (Callable): The management command function to be decorated.

    Returns:
        Callable: The decorated management command function.
    """

    def inner(self, *args, **kwargs) -> Any:
        params = {'sender': self.__class__, 'args': args, 'kwargs': kwargs}
        pre_command.send(**params)

        try:
            result = func(self, *args, **kwargs)
        except Exception as e:
            params['outcome'] = e
            post_command.send(**params)
            raise
        else:
            params['outcome'] = result
            post_command.send(**params)
            return result

    return inner
