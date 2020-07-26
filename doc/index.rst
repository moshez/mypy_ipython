MyPy IPython
============

.. toctree::
   :hidden:
   :maxdepth: 2

   demo

Type check your Jupyter notebooks!

Introduction
------------

The
:code:`mypy_ipython`
extension integrates the
mypy_
type checker with
Jupyter_ notebooks.

.. _IPython: https://ipython.readthedocs.io/en/stable/
.. _mypy: https://mypy.readthedocs.io/en/stable/ 
.. _Jupyter: https://jupyter.org/


Quick Start
-----------

Load the extension with:

.. code::

    %load_ext mypy_ipython

Then run the type check with:

.. code::

    %mypy

Example output:

.. code:: none

    note: In function "foo":
           x + "d"
    error: Unsupported operand types for + ("int" and "str")
           return {}
    error: Incompatible return value type (got "Dict[<nothing>, <nothing>]", expected "str")
    Found 2 errors in 1 file (checked 1 source file)

    Type checking failed
