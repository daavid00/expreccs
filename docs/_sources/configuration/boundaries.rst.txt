Boundary conditions and projection
==================================

Boundary settings determine how the regional and site models communicate.
Regional boundaries describe the outer aquifer, while site boundaries can use
static conditions or dynamically projected regional results.

Regional boundary conditions
----------------------------

``regional_bctype`` accepts ``open``, ``closed``, or ``porv``. For ``porv``,
append bottom, right, top, and left pore-volume values.

.. code-block:: toml

   regional_bctype = ["open"]

Site boundary conditions
------------------------

``site_bctype`` accepts:

``open``
   Use open site boundaries.

``closed``
   Use closed site boundaries.

``porv``
   Apply user-provided pore volumes in bottom, right, top, and left order.

``porvproj``
   Add pore volumes calculated from the regional reservoir.

``flux``
   Project regional fluxes to the site boundaries.

``pres``
   Project pressures using all available regional pressures along each side.

``pres2p``
   Project pressures using two points for each side.

``wells``
   Add four injectors and four producers at the site-boundary midpoints.

.. code-block:: toml

   site_bctype = ["open"]

Temporal interpolation
----------------------

For ``pres`` and ``flux`` conditions, add ``interp`` to use linear interpolation
in time. Existing-deck workflows also expose projection frequency and
telescopic time-partition controls through the command line.

Comparison workflows
--------------------

The reference model provides the high-resolution comparison solution. The
regional simulation supplies the projected boundary information, and the site
simulation evaluates how well each boundary treatment reproduces the reference
behavior. See :doc:`../examples/hello-world` for flux, pressure,
projected-pore-volume, and boundary-well examples.
