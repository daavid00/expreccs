ECMOR 2026
==========

Publication
-----------

This page describes how to reproduce the results in:

* Landa-Marbán, D., Sandve, T. H., and Gasda, S. E. (2026). Improving
  pressure communication in coarsened aquifer models for CO2 storage via
  explicit non-net cell treatment. ECMOR 2026.

The workflows use Bash scripts for most tasks and Python scripts for the more
comprehensive processing steps.

Prerequisites
-------------

The main preprocessing and postprocessing tools are
`pycopm <https://github.com/cssr-tools/pycopm>`_ and
`plopm <https://github.com/cssr-tools/plopm>`_. Install their current
development versions with:

.. code-block:: console

   pip install git+https://github.com/cssr-tools/pycopm.git
   pip install git+https://github.com/cssr-tools/plopm.git

The Troll workflow also requires OPM Flow. Some figures require PowerPoint,
ParaView, or ResInsight for manual assembly or screenshots, as described in the
corresponding sections.

Method: Figure 1
----------------

Run ``figure1.sh`` from the
``publications/ecmor2026/method`` directory:

.. code-block:: console

   . ./figure1.sh

.. note::

   PowerPoint is used to assemble the subfigures and add the colored
   connections.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/method/figure1.sh
         :color: primary
         :outline:
         :expand:

         View figure1.sh

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/method/figure1.sh
         :color: primary
         :outline:
         :expand:

         View raw figure1.sh

2D synthetic model
------------------

Run ``figure2.sh`` and ``figure3_table1.py`` from the
``publications/ecmor2026/results_2d_synthetic_model`` directory:

.. code-block:: console

   . ./figure2.sh
   python3 figure3_table1.py

.. note::

   PowerPoint is used to add the sensor, region, and well annotations to
   Figure 2.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_2d_synthetic_model/figure2.sh
         :color: primary
         :outline:
         :expand:

         View figure2.sh

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_2d_synthetic_model/figure2.sh
         :color: primary
         :outline:
         :expand:

         View raw figure2.sh

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_2d_synthetic_model/figure3_table1.py
         :color: primary
         :outline:
         :expand:

         View figure3_table1.py

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_2d_synthetic_model/figure3_table1.py
         :color: primary
         :outline:
         :expand:

         View raw figure3_table1.py

3D synthetic model
------------------

Run ``figure4_table2.py`` from the
``publications/ecmor2026/results_3d_synthetic_model`` directory:

.. code-block:: console

   python3 figure4_table2.py

.. note::

   The graphics in Figure 4 are generated from screenshots using
   `ParaView <https://www.paraview.org/>`_.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_3d_synthetic_model/figure4_table2.py
         :color: primary
         :outline:
         :expand:

         View figure4_table2.py

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_3d_synthetic_model/figure4_table2.py
         :color: primary
         :outline:
         :expand:

         View raw figure4_table2.py

Troll aquifer model
-------------------

The ``MODEL.DATA`` and ``FILLED_MODEL.DATA`` decks have the same dimensions and
total number of cells, 12,450,809, as the Troll aquifer model. Their remaining
properties use common homogeneous literature values, while the well locations
match those described in the ECMOR 2026 paper.

The repository does not distribute the actual Troll aquifer model. Contact the
`Norwegian Offshore Directorate <https://www.sodir.no/en/>`_ to obtain the
model, then adapt the supplied files in the
`results_troll/results directory
<https://github.com/cssr-tools/expreccs/tree/main/publications/ecmor2026/results_troll/results>`_.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_troll/results/MODEL.DATA
         :color: secondary
         :outline:
         :expand:

         View MODEL.DATA

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_troll/results/FILLED_MODEL.DATA
         :color: secondary
         :outline:
         :expand:

         View FILLED_MODEL.DATA

.. warning::

   Do not run ``MODEL.DATA`` or ``FILLED_MODEL.DATA`` before adapting them to
   the actual Troll aquifer model. The supplied layouts contain many active
   cells and are not substitutes for the authority-provided model.

Prepare the filled model
------------------------

Using the Petrel model provided by the Norwegian Offshore Directorate, export
the non-net cell identifiers to ``FLUXNUM`` and assign those entries a value of
zero. Then use ``EQUALREG`` to assign ``PORO`` and permeability values in the
non-net cells. See ``FILLED_MODEL.DATA`` for the implemented keyword pattern.

Run the Troll simulations
-------------------------

Create the dual models and run all simulations with ``run_results.sh`` from the
``publications/ecmor2026/results_troll`` directory:

.. code-block:: console

   . ./run_results.sh

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_troll/run_results.sh
         :color: primary
         :outline:
         :expand:

         View run_results.sh

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_troll/run_results.sh
         :color: primary
         :outline:
         :expand:

         View raw run_results.sh

Generate Table 3
----------------

Generate Table 3 with ``table3.py``:

.. code-block:: console

   python3 table3.py

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_troll/table3.py
         :color: primary
         :outline:
         :expand:

         View table3.py

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_troll/table3.py
         :color: primary
         :outline:
         :expand:

         View raw table3.py

Generate Figures 5 to 9
-----------------------

Generate Figures 5 to 9 with ``figure5-9.sh``:

.. code-block:: console

   . ./figure5-9.sh

.. note::

   Figures 5c and 5d are generated from screenshots using
   `ResInsight <https://resinsight.org>`_. PowerPoint is used to add the wells
   in Figure 7 and to assemble Figure 9 from ``figure9a.png``,
   ``figure9b.png``, and ``figure9c.png``. The color bar is taken from
   ``to_extract_colorbar_for_figure9.png``.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/publications/ecmor2026/results_troll/figure5-9.sh
         :color: primary
         :outline:
         :expand:

         View figure5-9.sh

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/publications/ecmor2026/results_troll/figure5-9.sh
         :color: primary
         :outline:
         :expand:

         View raw figure5-9.sh
