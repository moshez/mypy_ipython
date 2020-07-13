import functools
import sys

from . import recorder, check_cells

OUTPUT_TARGETS = {
    check_cells.Severity.NORMAL: sys.stdout,
    check_cells.Severity.ERROR: sys.stderr,
}


def check_recorded_cells(my_recorder, _ignored):
    snippets = my_recorder.relevant_snippets()
    results = check_cells.check(snippets)
    check_cells.output(results, OUTPUT_TARGETS)


def load_ipython_extension(ipython):
    my_recorder = recorder.Recorder()
    my_post_execute = functools.partial(recorder.post_execute, my_recorder, ipython)
    ipython.events.register("post_execute", my_post_execute)
    ipython.register_magic_function(
        functools.partial(check_recorded_cells, my_recorder),
        magic_kind="line",
        magic_name="mypy",
    )
