import setuptools

with open("README.rst") as fp:
    long_description = fp.read()

setuptools.setup(
    name="mypy_ipython",
    license="MIT",
    description="",
    long_description=long_description,
    use_incremental=True,
    setup_requires=["incremental"],
    author="Moshe Zadka",
    author_email="moshez@zadka.club",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["attrs", "incremental", "mypy", "IPython"],
    extras_require=dict(
        test=["pytest", "coverage"],
        lint=["black", "flake8", "mypy"],
        doc=["sphinx", "nbsphinx"],
    ),
    url="https://github.com/moshez/mypy_ipython",
    project_urls={
        "Documentation": "https://mypy-ipython.readthedocs.io/en/latest/",
        "Source": "https://github.com/moshez/mypy_ipython",
    },
)
