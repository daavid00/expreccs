Layered model
=============

The configuration file example2.toml set a more complex geological model with more grid cells (1 417 500). This was used
to generate the animation (using `ResInsight <https://resinsight.org>`_) in the :doc:`introduction section <../introduction>` by running

.. code-block:: bash

    expreccs -i example2.toml -m reference

.. tip::

    This example shows how **expreccs** can be used to generate the required input files to run OPM Flow for heterogenous
    layered models at different grid sizes, which can be used for further studies such as optimization. Regarding the configuration 
    files in `examples/paper_2025 <https://github.com/cssr-tools/expreccs/tree/main/examples/paper_2025>`_, these are explained in 
    `this manuscript <https://doi.org/10.1016/j.geoen.2025.213733>`_.

==================

.. button-ref:: ../examples
   :color: primary

   Back to examples gallery
