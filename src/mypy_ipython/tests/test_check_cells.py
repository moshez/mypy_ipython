from mypy_ipython import check_cells

import io
import textwrap

def test_check():
    cells = list(map(textwrap.dedent, [
    """\
    from typing import List
    def foo(special_parameter: int) -> List:
        y = special_parameter +  "hello"
        return 314159
    """]))
    ret_value = list(check_cells.check(cells))
    assert ret_value[-1][0] == check_cells.Severity.ERROR 
    ret_value.pop()
    assert set(x[0] for x in ret_value) == {check_cells.Severity.NORMAL} 
    explanations = [x[1] for x in ret_value]
    errors = [explanation for explanation in explanations if explanation.startswith("error:")]
    assert errors[0].startswith("error: Unsupported operand types")
    assert errors[1].startswith("error: Incompatible return value")
    assert len(errors) == 2
    for error in errors:
        explanations.remove(error)
    assert 'foo' in explanations[0]
    explanations.pop(0)
    assert 'special_parameter' in explanations[0]
    explanations.pop(0)
    assert '314159' in explanations[0]
    explanations.pop(0)
    assert len(explanations) <= 1

def test_check_successful():
    cells = list(map(textwrap.dedent, [
    """\
    from typing import List
    def foo() -> int:
        return 1
    """]))
    ret_value = list(check_cells.check(cells))
    assert ret_value[-1][0] == check_cells.Severity.NORMAL 
    ret_value.pop()
    assert set(x[0] for x in ret_value) == {check_cells.Severity.NORMAL} 
    assert ret_value[-1][1].startswith("Success")
    ret_value.pop()
    assert ret_value == []


def test_output():
    outputs = {check_cells.Severity.NORMAL: io.StringIO()}
    check_cells.output([(check_cells.Severity.NORMAL, "hello")], outputs)
    assert outputs[check_cells.Severity.NORMAL].getvalue() == "hello\n"
