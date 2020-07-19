from mypy_ipython import recorder

def test_recorder():
    arecorder = recorder.Recorder()
    arecorder.process("x=1\n")
    assert arecorder.relevant_snippets() == ["x=1\n"]

def test_recorder_syntax_error():
    arecorder = recorder.Recorder()
    arecorder.process("x=1\n")
    arecorder.process("???\n")
    assert arecorder.relevant_snippets() == ["x=1\n"]
