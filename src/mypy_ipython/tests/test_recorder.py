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

def test_recorder_function():
    arecorder = recorder.Recorder()
    arecorder.process("def foo(): pass\n")
    assert arecorder.relevant_snippets() == ["def foo(): pass\n"]

def test_recorder_function_redefinition():
    arecorder = recorder.Recorder()
    arecorder.process("def foo(): pass\n")
    arecorder.process("def foo(): print(5)\n")
    assert arecorder.relevant_snippets() == ["def foo(): print(5)\n"]
