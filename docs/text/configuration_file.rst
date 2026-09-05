Configuration reference
=======================

A TOML configuration file defines an integrated **expreccs** study: the
reference model, the coarser regional model, the embedded site model, dynamic
boundary conditions, rock and saturation properties, wells, and the simulation
schedule.

Use a configuration file when expreccs should generate and run the models. To
project dynamic pressures between two existing OPM Flow decks instead, use the
:doc:`existing-deck examples <examples/regular-boundaries>` and the
:doc:`command-line reference <command-line>`.

The pages below explain related settings together. The final page contains only
the complete annotated TOML file, making it easier to copy and modify without
repeating the explanatory figures and prose.

.. toctree::
   :maxdepth: 1

   configuration/integrated
   configuration/boundaries
   configuration/properties
   configuration/wells
   configuration/complete
