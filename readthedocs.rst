readthedocs
===========

- use restructured text 

sphinx
------
pip install sphinx
sphinx-quickstart



integration github
------------------

https://readthedocs.org/dashboard/


*include .readthedocs.yml in github repository*

.. code-block:: bash

   version: 2

   build:
      os: ubuntu-22.04
      tools:
         python: "3.12"

   sphinx:
      configuration: conf.py



