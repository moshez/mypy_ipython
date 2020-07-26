from __future__ import annotations

import ast
import collections
from typing import Dict, Iterable, TYPE_CHECKING
import attr

if TYPE_CHECKING:
    import IPython  # pragma: no cover


@attr.s(auto_attribs=True)
class Recorder:
    _record: Dict[int, str] = attr.ib(init=False, factory=collections.OrderedDict)
    _running: int = attr.ib(init=False, default=0)
    _top_levels: Dict[str, int] = attr.ib(init=False, factory=dict)

    def process(self, snippet: str) -> None:
        def get_top_level() -> Iterable[str]:
            module = compile(snippet, "", "exec", ast.PyCF_ONLY_AST)
            for top_level in module.body:
                if isinstance(top_level, (ast.ClassDef, ast.FunctionDef)):
                    yield top_level.name

        try:
            all_top_levels = list(get_top_level())
        except SyntaxError:
            return
        self._running += 1
        self._record[self._running] = snippet
        for top_level in all_top_levels:
            if top_level in self._top_levels:
                snippet_id = self._top_levels[top_level]
                if snippet_id in self._record:
                    del self._record[snippet_id]
            self._top_levels[top_level] = self._running

    def relevant_snippets(self) -> Iterable[str]:
        return list(self._record.values())


def consume_history(
    recorder: Recorder, shell: IPython.core.interactiveshell.InteractiveShell
) -> None:
    for cell in shell.history_manager.input_hist_parsed:
        recorder.process(cell)


def post_execute(
    recorder: Recorder, shell: IPython.core.interactiveshell.InteractiveShell
) -> None:
    recorder.process(shell.history_manager.input_hist_parsed[-1])
