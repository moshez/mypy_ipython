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

Via `anaconda cloud <https://anaconda.org/laura-dietz/mypy-ipython>`_.

Note that this needs to be installed in the environment
that your kernel is running in.
This will usually be the environment running your Jupyter server.

Quick Start
-----------

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
