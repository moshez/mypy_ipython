from __future__ import annotations

from typing import List, Iterable, Tuple

from mypy import api as mypy_api

import enum
import re
import sys


@enum.unique
class Severity(enum.Enum):
    NORMAL = enum.auto()
    ERROR = enum.auto()


DIGITS = re.compile(r"\d+")


def lines(
    normal_report: str, error_report: str, status: str, input_data: str
) -> Iterable[Tuple[Severity, str]]:
    input_lines = input_data.splitlines()
    for line in normal_report.splitlines():
        if line.startswith("<string>:"):
            line = line[len("<string>:") :]
        match = DIGITS.match(line)
        if not match:
            yield Severity.NORMAL, line.strip()
            continue
        line_num = match.group()
        idx = int(match.group()) - 1
        offending_line = input_lines[idx][:50]
        yield Severity.NORMAL, "    " + offending_line
        yield Severity.NORMAL, line[match.end() + 1 :].strip()
    for line in error_report.splitlines():
        yield Severity.ERROR, line
    if status == 0:
        yield Severity.NORMAL, "Type checking successful"
    else:
        yield Severity.ERROR, "Type checking failed"


def output(stream, outputs):
    for severity, content in stream:
        print(content, file=outputs[severity])


def check(cells: List[str]):
    cells = ["from IPython import get_ipython"] + cells
    input_data = "\n".join(cells)
    normal_report, error_report, status = mypy_api.run(
        ["-c", input_data, "--ignore-missing-imports", "--show-error-context"]
    )
    return lines(normal_report, error_report, status, input_data)
