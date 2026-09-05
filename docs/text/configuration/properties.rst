Rock, saturation, hysteresis, and salinity
==========================================

This page defines the saturation-function expressions, layer-dependent
saturation parameters, rock properties, optional hysteresis, and salinity.

Saturation-function expressions
-------------------------------

``krw``, ``krn``, and ``pcap`` are Python expressions for wetting relative
permeability, non-wetting relative permeability, and capillary pressure.

.. code-block:: toml

   krw = "krw * ((sw - swi) / (1.0 - sni - swi)) ** nkrw"
   krn = "krn * ((1.0 - sw - sni) / (1.0 - sni - swi)) ** nkrn"
   pcap = "pen * ((sw - swi) / (1.0 - swi)) ** (-(1.0 / npen))"

Saturation properties
---------------------

Each ``safu`` row contains:

#. Irreducible wetting saturation, ``swi``.
#. Residual non-wetting saturation, ``sni``.
#. End-point wetting relative permeability, ``krw``.
#. End-point non-wetting relative permeability, ``krn``.
#. Entry pressure in bar, ``pen``.
#. Wetting relative-permeability exponent, ``nkrw``.
#. Non-wetting relative-permeability exponent, ``nkrn``.
#. Capillary-pressure exponent, ``npen``.
#. Capillary-pressure evaluation threshold.
#. Number of saturation-table points.

Provide one drainage row per layer. When hysteresis is enabled, append one
imbibition row per layer. The complete 18-row example is retained in
:doc:`complete`.

Rock properties
---------------

Each ``rock`` row contains horizontal permeability in mD, vertical permeability
in mD, and porosity. Provide one row per layer.

.. code-block:: toml

   rock = [
       [1013.25, 101.325, 0.25],
       [506.625, 50.6625, 0.20],
       [1013.25, 101.325, 0.25],
       [506.625, 50.6625, 0.20],
       [0.10132, 0.01013, 0.10],
       [101.324, 10.1324, 0.20],
       [202.650, 20.2650, 0.20],
       [101.324, 10.1324, 0.20],
       [202.650, 20.2650, 0.20],
   ]

Hysteresis
----------

``hysteresis`` is optional. Its first entry selects ``Killough`` or ``Carlson``;
the second selects ``Both``, ``Pc``, or ``Kr``. Omitting the variable disables
hysteresis. In the complete example, imbibition rows change residual saturation
to 0.3 and the non-wetting exponent to 4.

.. code-block:: toml

   hysteresis = ["Killough", "Both"]

Salinity
--------

``salinity`` adds salt concentration in units of ``1e-3 kg-M/kg``.

.. code-block:: toml

   salinity = 2.92
