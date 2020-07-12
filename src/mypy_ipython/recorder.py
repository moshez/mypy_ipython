from __future__ import annotations

from typing import List, Dict
import attr
import collections


@attr.s(auto_attribs=True)
class Recorder:
    _record: Dict[int, str] = attr.ib(init=False, factory=collections.OrderedDict)
    _running: int = attr.ib(init=False, default=0)
    _top_levels: Dict[str, int] = attr.ib(init=False, factory=dict)

    def process(self, snippet):
        def get_top_level():
            try:
                module = compile(snippet, "", "exec", ast.PyCF_ONLY_AST)
            except SyntaxError:
                return
            for top_level in module.body:
                if isinstance(top_level, (ast.ClassDef, ast.FunctionDef)):
                    yield top_level.name

        self._running += 1
        self._record[self._running] = snippet
        for top_level in get_top_level():
            if top_level in self._top_levels:
                snippet_id = self._top_levels[top_level]
                if snippet_id in self._record:
                    del self._record[snippet_id]
            self._top_levels[top_level] = self._running

    def relevant_snippets(self):
        return list(self._record.values())


def post_execute(
    recorder: Recorder, shell: IPython.core.interactiveshell.InteractiveShell
):
    recorder.process(shell.history_manager.input_hist_parsed[-1])
