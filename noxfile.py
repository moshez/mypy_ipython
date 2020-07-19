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
        "coverage", "run", "--source=src/mypy_ipython",
        "-m", "pytest", *tests,
        env=dict(COVERAGE_FILE=os.path.join(tmpdir, "coverage")),
    )
    fail_under = "--fail-under=100"
    session.run("coverage", "report", fail_under, "--show-missing",
        "--skip-covered",
        env=dict(COVERAGE_FILE=os.path.join(tmpdir, "coverage")),
    )
    session.notify("cover")


@nox.session(python="3.8")
def lint(session):
    session.install("flake8==3.7.8", "black==19.3b0", "mypy==0.720")
    session.run(
        "mypy",
        "--disallow-untyped-defs",
        "--warn-unused-ignores",
        "--ignore-missing-imports",
        "src/mypy_ipython",
    )
    files = ["src/mypy_python", "noxfile.py", "setup.py"]
    session.run("black", "--check", *files)
    session.run("flake8", "--max-line-length=88", "src/mypy_ipyton")


@nox.session(python="3.8")
def docs(session):
    """Build the documentation."""
    output_dir = os.path.join(session.create_tmp(), "output")
    doctrees, html = map(
        functools.partial(os.path.join, output_dir), ["doctrees", "html"]
    )
    session.run("rm", "-rf", output_dir, external=True)
    session.install(".[docs]")
    session.cd("docs")
    sphinx_args = ["-b", "html", "-W", "-d", doctrees, ".", html]

    if not session.interactive:
        sphinx_cmd = "sphinx-build"
    else:
        sphinx_cmd = "sphinx-autobuild"
        sphinx_args.insert(0, "--open-browser")

    session.run(sphinx_cmd, *sphinx_args)
