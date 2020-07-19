import functools
import io
import sys
from typing import Any, Dict

import IPython

from . import recorder, check_cells
from ._version import __version__


def check_recorded_cells(my_recorder: recorder.Recorder, _ignored: Any) -> None:
    # Ignoring problems because of https://github.com/python/typeshed/issues/1240#issuecomment-660716422 # noqa: E501
    output_targets: Dict[check_cells.Severity, io.TextIOBase] = {
        check_cells.Severity.NORMAL: sys.stdout,  # type: ignore
        check_cells.Severity.ERROR: sys.stderr,  # type: ignore
    }
    snippets = my_recorder.relevant_snippets()
    results = check_cells.check(snippets)
    check_cells.output(results, output_targets)


def load_ipython_extension(
    ipython: IPython.core.interactiveshell.InteractiveShell,
) -> None:
    my_recorder = recorder.Recorder()
    my_post_execute = functools.partial(recorder.post_execute, my_recorder, ipython)
    ipython.events.register("post_execute", my_post_execute)
    ipython.register_magic_function(
        functools.partial(check_recorded_cells, my_recorder),
        magic_kind="line",
        magic_name="mypy",
    )


__all__ = ["load_python_extension", "__version__"]
