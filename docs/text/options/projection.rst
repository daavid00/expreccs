Boundary-projection options
===========================

Skipped boundary entries
------------------------

``-b`` skips entries in bottom, right, top, and left order.

Temporal interpolation
----------------------

``-f`` controls the number of boundary-pressure evaluations between site report steps. ``-a`` controls the exponential telescopic partition and accepts zero for equidistant spacing.

Pressure representation
-----------------------

``-e 0`` writes regional pressure increase instead of absolute pressure.

FIPNUM mapping
--------------

``-z 1`` projects pressures per matching FIPNUM zones.

Irregular contours
------------------

``-n 1`` enables a non-rectangular site boundary.
