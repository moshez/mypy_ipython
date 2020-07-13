MyPy/Jupyter Integration
========================

Instructions:

* Install this (for example,
  ``pip install git+https://github.com/moshez/mypy_ipython.git``)
  in the virtual environment your kernel is running
  (usually the same virtual environment Jupyter is running).
* In a notebook, as early as possible,
  run ``%load_ext mypy_ipython``
  in a cell.
* Whenever you need to check the types, run
  ``%mypy``
  in a cell.
