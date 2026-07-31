from collections.abc import Callable

type TypeShellRunner = Callable[..., None]

type TypeDirectiveTuple = tuple[str, tuple[str, ...]]
