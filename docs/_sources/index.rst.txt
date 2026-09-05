expreccs
========

.. rst-class:: lead

   A framework for dynamic regional-to-site boundary conditions in CO2 storage
   simulations.

**expreccs** creates integrated regional, reference, and site models and
projects dynamic boundary conditions between nonconforming OPM Flow grids. It
supports pressure-interference studies, comparison of boundary treatments, and
reproducible regional-to-site modeling workflows.

.. grid:: 1 2 2 4
   :gutter: 3
   :margin: 4 0 4 0

   .. grid-item-card:: :octicon:`rocket;1.2em` Get started
      :link: introduction
      :link-type: doc

      Understand the two-stage regional-to-site workflow and project context.

   .. grid-item-card:: :octicon:`download;1.2em` Install
      :link: installation
      :link-type: doc

      Install expreccs, OPM Flow, and optional visualization tools.

   .. grid-item-card:: :octicon:`gear;1.2em` Configure a study
      :link: configuration_file
      :link-type: doc

      Define integrated reference, regional, and site models in TOML.

   .. grid-item-card:: :octicon:`book;1.2em` Explore examples
      :link: examples
      :link-type: doc

      Run integrated studies and project boundaries between existing decks.

Quick installation
------------------

Install the current development version:

.. code-block:: console

   pip install git+https://github.com/cssr-tools/expreccs.git

See :doc:`installation` for virtual environments, OPM Flow, ResInsight, plopm,
optional LaTeX support, and installation from source.

Quick start
-----------

Run an integrated regional, reference, and site study:

.. code-block:: console

   expreccs -i examples/example1.toml -o hello_world

Project dynamic boundary conditions between existing regional and site models:

.. code-block:: console

   expreccs -i "tests/regional/REGIONAL tests/site/SITE" -o projected

Display the available command-line options:

.. code-block:: console

   expreccs --help

See :doc:`examples` for complete workflows, :doc:`configuration_file` for TOML
settings, and :doc:`command-line` for exact syntax, accepted values, defaults,
and workflow compatibility.

What can expreccs do?
---------------------

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Build integrated studies

      Generate reference, regional, and site corner-point models with
      heterogeneous properties, faults, hysteresis, salinity, wells, and
      operational schedules.

   .. grid-item-card:: Project dynamic boundaries

      Map pressure, pressure increase, flux, and pore-volume effects from
      regional models to regular or irregular site boundaries.

   .. grid-item-card:: Compare modeling strategies

      Evaluate open, projected, two-point, per-FIPNUM, projected-pore-volume,
      and boundary-well approaches against a reference simulation.

   .. grid-item-card:: Support reproducible research

      Reproduce the 2025 hierarchical regional-to-site study using the
      configurations and scripts under ``examples/paper_2025``.

Related project publications
----------------------------

The repository also hosts two publication-reproduction workflows developed
within the broader expreccs research project. These workflows share the
project's OPM Flow, preprocessing, visualization, and reproducibility
infrastructure, but they do not use the **expreccs** Python executable.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: :octicon:`file;1.2em` TCCS-13
      :link: tccs-13
      :link-type: doc

      Reproduce the Troll aquifer coarsening and optimization study using OPM
      Flow, pycopm, plopm, Everest, and supporting scripts.

   .. grid-item-card:: :octicon:`file;1.2em` ECMOR 2026
      :link: ecmor2026
      :link-type: doc

      Reproduce the explicit non-net-cell treatment study using OPM Flow,
      pycopm, plopm, and supporting scripts.

.. toctree::
   :hidden:
   :maxdepth: 2

   introduction
   installation
   configuration_file
   examples
   tccs-13
   ecmor2026
   command-line
   api
   output_folder
   contributing
   related
