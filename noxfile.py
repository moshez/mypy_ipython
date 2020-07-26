import functools
import os

import nox

nox.options.envdir = "build/nox"


@nox.session(python=["3.7", "3.8"])
def tests(session):
    """Run test suite with pytest."""
    tmpdir = session.create_tmp()
    session.install("-e", ".[test]")
    tests = session.posargs or ["src/mypy_ipython/tests"]
    session.run(
        "coverage",
        "run",
        "--source=src/mypy_ipython",
        "-m",
        "pytest",
        *tests,
        env=dict(COVERAGE_FILE=os.path.join(tmpdir, "coverage")),
    )
    fail_under = "--fail-under=100"
    session.run(
        "coverage",
        "report",
        fail_under,
        "--show-missing",
        "--skip-covered",
        env=dict(COVERAGE_FILE=os.path.join(tmpdir, "coverage")),
    )


@nox.session(python="3.8")
def lint(session):
    files = ["src/mypy_ipython", "noxfile.py", "setup.py"]
    session.install("-e", ".[lint]")
    session.run("black", "--check", "--diff", *files)
    black_compat = ["--max-line-length=88", "--ignore=E203"]
    session.run("flake8", *black_compat, "src/mypy_ipython")
    session.run(
        "mypy",
        "--disallow-untyped-defs",
        "--warn-unused-ignores",
        "--ignore-missing-imports",
        "src/mypy_ipython",
    )


@nox.session(python="3.8")
def docs(session):
    """Build the documentation."""
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), "output"))
    doctrees, html = map(
        functools.partial(os.path.join, output_dir), ["doctrees", "html"]
    )
    session.run("rm", "-rf", output_dir, external=True)
    session.install(".[doc]")
    session.install("sphinx-autobuild")
    sphinx_args = ["-b", "html", "-W", "-d", doctrees, ".", html]


    if not session.interactive:
        sphinx_cmd = "sphinx-build"
    else:
        sphinx_cmd = "sphinx-autobuild"
        sphinx_args.insert(0, "--open-browser")

    session.cd("doc")
    session.run(sphinx_cmd, *sphinx_args)

