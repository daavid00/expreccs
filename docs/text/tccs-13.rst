TCCS-13
=======

Publication
-----------

Here we describe the steps to reproduce the results in:

* Landa-Marbán, D., Sandve, T.H., and Gasda, S.E., 2026. A coarsening approach to the troll aquifer model. In Nils Anders Røkke, Philip Stefan Ringrose, & Stefan Marcell Götz (Eds.), TCCS-13. CO2 Capture, Transport and Storage Trondheim, Norway | 16–19 June 2025 Short Papers from the 13th Trondheim CCS Conference (pp. 13–20). SINTEF akademisk forlag. https://hdl.handle.net/11250/5559902

Troll aquifer model access and preparation
------------------------------------------

To this end, the deck `ORIGINAL.DATA <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/ORIGINAL.DATA>`_ has the 
same dimensions and number of total cells (12,450,809) as the Troll aquifer model, and the rest of the properties are 
set to common homogeneous values from literature, while the well locations match the ones described in the TCCS-13 paper.
Then, you could contact the `Norwegian Offshore Directorate <https://www.sodir.no/en/>`_ to get the actual Troll aquifer model,
and adapt those files to the ones in the `tccs-13 folder <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/>`_.

.. warning::

    You should not run the ORIGINAL.DATA file before adapting it with the actual Troll aquifer model, since it has a lot of active cells.

Prerequisites
-------------

For the first figures, `plopm <https://github.com/cssr-tools/plopm>`_ and `pycopm <https://github.com/cssr-tools/pycopm>`_ are used, which can be installed by:

.. code-block:: bash

    pip install git+https://github.com/cssr-tools/plopm.git
    pip install git+https://github.com/cssr-tools/pycopm.git

To run the optimization, `Everest <https://github.com/equinor/everest-tutorials>`_ is needed,
which is installed via `ert <https://github.com/equinor/ert>`_ when pycopm is installed with the command above.

Methodology: Figures 1 and 2
----------------------------

The following commands generate Figures 1 and 2 (a few features such as the transmissibilities, wells, and sensor are added using PowerPoint) using 
`FIG1.DATA <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/methodology/FIG1.DATA>`_:

.. code-block:: bash

    pycopm -i FIG1.DATA -z 1:4 -m all -a max -w COARSENED_TRANS -l TRANS -t 2
    pycopm -i FIG1.DATA -c 1,1,4 -m all -a max -w COARSENED_PERMS -l PERMS
    flow FIG1.DATA
    flow COARSENED_TRANS.DATA
    flow COARSENED_PERMS.DATA
    plopm -i FIG1 -v poro -c '#bfebf2' -asp 0 -ge 'black,1e0' -y '[5,-1]' -ynt 5 -xnt 7 -r 0 -hide 0,0,1,1 -fs 24,16 -fz 60 -fn fig1
    plopm -i 'COARSENED_PERMS FIG1 COARSENED_TRANS' -v 'pressure - 0pressure' -sg 3,1 -r 1 -asp 0 -rdl 1 -y '[5,-1]' -cbf .0f -ge 'black,1e0' -cbp 0.1,0.95,0.8,0.02 -st 0 -cbl 'Pressure increase [bar]' -cbn 5 -t 'Coarsened (permeabilities)  Before coarsening  Coarsened (transmissibilities)' -fs 24,48 -fz 80 -fn fig2

Original and coarsened models
-----------------------------

For Figs. 3b, 5, 6, and 8, 9, and 10 using ORIGINAL.DATA in the `expreccs/tccs-13/original <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/original/>`_ folder:

.. code-block:: bash

    flow ORIGINAL.DATA --enable-opm-rst-file=true --linear-solver=cpr_trueimpes --time-step-control=newtoniterationcount --newton-min-iterations=1 --tolerance-cnv-relaxed=1e-2 --relaxed-max-pv-fraction=0
    pycopm -i ORIGINAL.DATA -t 2 -a max -z 1:30,31:56,57:111,112:116,117:217 -w COARSENED -l C
    flow COARSENED.DATA --enable-opm-rst-file=true --linear-solver=cpr_trueimpes --time-step-control=newtoniterationcount --newton-min-iterations=1 --tolerance-cnv-relaxed=1e-2 --relaxed-max-pv-fraction=0
    plopm -i ORIGINAL -v 'depth * 0.001' -s ,,1:217 -agg min -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -cbl 'Depth [km]' -cbn 5 -cbf .2f -c managua_r -fn fig3b
    plopm -i 'ORIGINAL ORIGINAL ORIGINAL' -v 'porv' -s ',,1:30 ,,57:111 ,,117:217' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,3 -fs 24,12 -cbp 0.1,0.95,0.8,0.02 -cbf .1f -fz 24 -cbn 5 -st 0 -cbl 'Total pore volume [m$^3$]' -clog 1 -c brg -t 'Cook  Johansen  Statfjord' -rdl 1 -fn fig5
    plopm -i 'ORIGINAL' -v 'faults' -s ',,1:217' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -fz 8 -gr 1 -t 'Total no. faults = 65' -fn fig6a
    plopm -i 'ORIGINAL' -v 'faults' -s ',,30:117' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -fz 8 -agg max -t 'Cook-Johansen-Statfjord' -hide 1,0,0,0 -fn fig6b
    plopm -i 'ORIGINAL ORIGINAL ORIGINAL' -v 'pressure - 0pressure' -s ',,1:30 ,,57:111 ,,117:217' -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,3 -fs  24,12 -cbp 0.1,0.95,0.8,0.02 -fz 24 -cbn 5 -st 0 -cbl 'Pore-volume-weighted-average pressure increase [bar]' -rdl 1 -r 25 -cl '[0,80]' -t 'Cook, t=25 years  Johansen, t=25 years  Statfjord, t=25 years' -cl '[0,80]' -fn fig8upper
    plopm -i 'ORIGINAL ORIGINAL ORIGINAL' -v 'pressure - 0pressure' -s ',,1:30 ,,57:111 ,,117:217' -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,3 -fs  24,12 -cbp 0.1,0.95,0.8,0.02 -fz 24 -cbn 5 -st 0 -cbl 'Pore-volume-weighted-average pressure increase [bar]' -rdl 1 -r 30 -cl '[0,80]' -t 'Cook, t=525 years  Johansen, t=525 years  Statfjord, t=525 years' -cl '[0,80]' -fn fig8lower
    plopm -i 'ORIGINAL ORIGINAL ORIGINAL' -v 'limipres' -s ',,1:30 ,,57:111 ,,117:217' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,3 -fs 24,12 -cbp 0.1,0.95,0.8,0.02 -cbf .1f -fz 24 -cbn 5 -st 0 -cbl 'Maximum allowable pressure increase limit [bar]' -c gnuplot2 -t 'Cook  Johansen  Statfjord' -rdl 1 -fn fig9
    plopm -i 'ORIGINAL' -v 'imbnum' -s ',,1:217' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -hide 0,0,1,1 -c '203;203;203' -fn fig10a
    plopm -i 'ORIGINAL COARSENED' -v 'overpres' -s ',,1:217 ,,1:5' -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,2 -fs 16,12 -cbp 0.1,0.95,0.8,0.02 -fz 24 -cbn 5 -st 0 -cbl 'Overpressure (p - p$_{lim}$) [bar], t=25 years' -rdl 1 -hide 1,0,0,0 -t 'Troll aquifer model  Coarsened version' -cl '[-126.7,-1.1]' -c cet_diverging_rainbow_bgymr_45_85_c67 -fn fig10bc

ResInsight figures
++++++++++++++++++

Figs. 4 and 7 are generated using `ResInsight <https://resinsight.org>`_. 
 
Everest optimization
--------------------

Using the coarsened files from pycopm, you could adapt the existing files in the `coarsened folder <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/coarsened/>`_ to run the optimization:

.. code-block:: bash

    everest run coarsened.yml --skip-prompt

.. note::

    You might need to adapt the number of cores and mpirun depending on your resources, i.e., the current file is set to use mpirun -np 5 flow ... and 14 cores in parallel.

Figure 11: optimization results
+++++++++++++++++++++++++++++++

After the study, to generate Fig. 11, execute the `postprocessing.py file <https://github.com/cssr-tools/expreccs/blob/main/tccs-13/postprocessing.py>`_:

.. code-block:: bash

    python3 postprocessing.py

Figure 12: improved well locations
----------------------------------

Finally, you can look at the improved well locations in the generated figures/optimal_solution folder, and take those locations into the ORIGINAL.DATA deck 
and save it as IMPROVED.DATA, similar to the coarsened version to COARSENED_IMPROVED.DATA, to generate Fig. 12:

.. code-block:: bash
    
    flow IMPROVED.DATA --enable-opm-rst-file=true --linear-solver=cpr_trueimpes --time-step-control=newtoniterationcount --newton-min-iterations=1 --tolerance-cnv-relaxed=1e-2 --relaxed-max-pv-fraction=0
    flow COARSENED_IMPROVED.DATA --enable-opm-rst-file=true --linear-solver=cpr_trueimpes --time-step-control=newtoniterationcount --newton-min-iterations=1 --tolerance-cnv-relaxed=1e-2 --relaxed-max-pv-fraction=0
    plopm -i 'IMPROVED' -v 'imbnum' -s ',,1:217' -r 0 -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -hide 0,0,1,1 -c '203;203;203' -fn fig12a
    plopm -i 'IMPROVED COARSENED_IMPROVED' -v 'overpres' -s ',,1:217 ,,1:5' -tr '[-495000,-6.605e6]' -x '[0,95000]' -xu km -xnt 2 -y '[0,160000]' -yu km -yf .0f -ynt 2 -xf .0f -sg 1,2 -fs 16,12 -cbp 0.1,0.95,0.8,0.02 -fz 24 -cbn 5 -st 0 -cbl 'Overpressure (p - p$_{lim}$) [bar], t=25 years' -rdl 1 -hide 1,0,0,0 -t 'Troll aquifer model  Coarsened version' -cl '[-126.7,-1.1]' -c cet_diverging_rainbow_bgymr_45_85_c67 -fn fig10bc


Reproducibility links
---------------------

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/tccs-13/ORIGINAL.DATA
         :color: primary
         :outline:
         :expand:

         View ORIGINAL.DATA

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/tccs-13/ORIGINAL.DATA
         :color: primary
         :outline:
         :expand:

         View raw ORIGINAL.DATA

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/tccs-13/methodology/FIG1.DATA
         :color: primary
         :outline:
         :expand:

         View FIG1.DATA

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/tccs-13/methodology/FIG1.DATA
         :color: primary
         :outline:
         :expand:

         View raw FIG1.DATA

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/expreccs/blob/main/tccs-13/postprocessing.py
         :color: primary
         :outline:
         :expand:

         View postprocessing.py

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/expreccs/main/tccs-13/postprocessing.py
         :color: primary
         :outline:
         :expand:

         View raw postprocessing.py

