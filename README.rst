MyPy/Jupyter Integration
========================

Instructions:

* Install this (for example,
  ``pip install mypy-ipython``)
  in the virtual environment your kernel is running
  (usually the same virtual environment Jupyter is running).
* Run
  ``%load_ext mypy_ipython``
  in a notebook cell.
* Whenever you need to check the types, run
  ``%mypy``
  in a cell.
