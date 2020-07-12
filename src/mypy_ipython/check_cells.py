from __future__ import annotations

from typing import List, Iterable, Tuple

from mypy import api as mypy_api

import enum
import sys


@enum.unique
class Severity(enum.Enum):
    NORMAL = enum.auto()
    ERROR = enum.auto()


def lines(
    normal_report: str, error_report: str, status: str
) -> Iterable[Tuple[Severity, str]]:
    for line in normal_report.splitlines():
        yield Severity.NORMAL, line
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
    normal_report, error_report, status = mypy_api.run(["-c", "\n".join(cells), "--ignore-missing-imports"])
    return lines(normal_report, error_report, status)
