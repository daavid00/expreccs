===================
expreccs Python API
===================

The main script for the **expreccs** executable is located in the core folder.
The expreccss folder contains mako files to generate the corresponding opm
input decks. The scripts in the utils folder process the input configuration
file, runs the reference, regional, and site simulations, in addition to include 
routines to project the pressures for given generic geological models. The scripts in the 
visualization folder generate images (.png) to show comparisons between the different runs.

.. figure:: figs/contents.png

    Files in the expreccs package.

.. include:: modules.rst