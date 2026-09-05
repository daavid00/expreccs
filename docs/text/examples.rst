Examples
========

The examples cover both ways of using **expreccs**: integrated studies defined
by TOML configuration files and dynamic boundary projection between existing
regional and site OPM Flow decks. Every command, figure, caption, projection
option, and reproduction script from the original documentation is retained in
the focused pages below.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Hello world
      :class-card: example-card
      :img-top: figs/hello_world_sensor_pressure_over_time.png
      :link: examples/hello-world
      :link-type: doc

      Run reference, regional, and site models with flux, pressure,
      projected-pore-volume, and boundary-well conditions.

   .. grid-item-card:: Layered model
      :class-card: example-card
      :img-top: figs/introduction.gif
      :link: examples/layered-model
      :link-type: doc

      Generate the 1,417,500-cell heterogeneous layered reference model.

   .. grid-item-card:: Regular boundaries
      :class-card: example-card
      :img-top: figs/reference_sgas.png
      :link: examples/regular-boundaries
      :link-type: doc

      Project dynamic boundaries between existing decks, including per-FIPNUM
      and pressure-increase interpolation.

   .. grid-item-card:: Non-regular boundaries
      :class-card: example-card
      :img-top: figs/expreccs_opernum_i,j,1_t0.png
      :link: examples/non-regular-boundaries
      :link-type: doc

      Refine and extract a polygonal site model, then project pressures to its
      irregular contour.

.. toctree::
   :hidden:
   :maxdepth: 1

   examples/hello-world
   examples/layered-model
   examples/regular-boundaries
   examples/non-regular-boundaries
