from __future__ import annotations

import enum
import re
from typing import Iterable, Tuple, Mapping
from typing_extensions import Protocol

from mypy import api as mypy_api


@enum.unique
class Severity(enum.Enum):
    NORMAL = enum.auto()
    ERROR = enum.auto()


DIGITS = re.compile(r"\d+")


def lines(
    normal_report: str, error_report: str, status: int, input_data: str
) -> Iterable[Tuple[Severity, str]]:
    input_lines = input_data.splitlines()
    for line in normal_report.splitlines():
        if line.startswith("<string>:"):
            line = line[len("<string>:") :]
        match = DIGITS.match(line)
        if not match:
            yield Severity.NORMAL, line.strip()
            continue
        idx = int(match.group()) - 1
        offending_line = input_lines[idx][:50]
        yield Severity.NORMAL, "    " + offending_line
        yield Severity.NORMAL, line[match.end() + 1 :].strip()
    if error_report != "":  # pragma: no cover
        raise ValueError("mypy running problem, this is probably a bug", error_report)
    if status == 0:
        yield Severity.NORMAL, "Type checking successful"
    else:
        yield Severity.ERROR, "Type checking failed"


class WritableTextFile(Protocol):
    def write(self, content: str) -> int:
        """Write a string."""


def output(
    stream: Iterable[Tuple[Severity, str]], outputs: Mapping[Severity, WritableTextFile]
) -> None:
    for severity, content in stream:
        print(content, file=outputs[severity])


def check(cells: Iterable[str]) -> Iterable[Tuple[Severity, str]]:
    my_cells = ["from IPython import get_ipython"]
    my_cells.extend(cells)
    input_data = "\n".join(my_cells)
    normal_report, error_report, status = mypy_api.run(
        ["-c", input_data, "--ignore-missing-imports", "--show-error-context"]
    )
    return lines(normal_report, error_report, status, input_data)
