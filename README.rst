MyPy/Jupyter Integration
========================

`Full documentation`_

.. _Full documentation: https://mypy-ipython.readthedocs.io/en/latest/

Installing
----------

pip
~~~

.. code::

    $ pip install mypy_ipython

Anaconda
~~~~~~~~

.. code::

    $ conda install -c laura-dietz mypy-ipython


Quick Start
-----------

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

Contributing
------------

* All contributions must follow our Code of Conduct.
* In your first pull request, please add yourself to the contributor list.

Contributors
------------

* `Moshe Zadka <moshez@zadka.club>`_
* `Laura Dietz`
