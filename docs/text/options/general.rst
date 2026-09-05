General options
===============

.. program:: expreccs

Input
-----

.. option:: -i <input>, --input <input>

   TOML configuration file, or quoted paths to regional and site model bases. Default: ``input.toml``.

Output
------

.. option:: -o <folder>, --output <folder>

   Output folder. Default: ``output``.

Mode
----

.. option:: -m <mode>, --mode <mode>

   Run ``all``, ``reference``, ``site``, ``regional``, ``regional_site``, or ``none``. Default: ``all``.

Comparison and plots
--------------------

``-c compare`` generates metric plots for existing output folders. ``-p yes`` creates postprocessing figures.

Rotation and folder layout
--------------------------

``-t`` rotates the site model in degrees. ``-s 0`` writes generated files directly to the output directory without preprocessing, simulation, and postprocessing subfolders.
