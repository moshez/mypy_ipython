import io
from unittest import mock

import mypy_ipython


def test_load_ipython_extension(capfd):
    ipython = mock.MagicMock()
    mypy_ipython.load_ipython_extension(ipython)
    (name, post_execute), kwargs = ipython.events.register.call_args
    assert name == "post_execute"
    assert kwargs == {}
    [checker], kwargs = ipython.register_magic_function.call_args
    assert kwargs == dict(magic_kind="line", magic_name="mypy")
    ipython.history_manager.input_hist_parsed = ["x=1\n"]
    post_execute()
    with mock.patch("sys.stdout", new=io.StringIO()) as temp_stdout:
        checker(None)
    output = temp_stdout.getvalue()
    assert output.startswith("Success")
