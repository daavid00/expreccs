flow METHOD --output-dir=figure1
pycopm -i METHOD.DATA -t 2 -a max -z 1:4 -l D -dual 'poro == 0.1' -o figure1
flow figure1/METHOD_PYCOPM
plopm -i figure1/METHOD -v 'fluxnum - 1' -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Input grid $\Omega$" -fn figure1a
plopm -i figure1/METHOD_PYCOPM -v 'fluxnum - 1' -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Standard $\Omega^{*}$" -gr 1 -hide 0,0,1,0 -fn figure1b
plopm -i figure1/METHOD_PYCOPM -v 'fluxnum - 1' -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Dual (vertical TF) $\Omega_\epsilon^{*,net}$, j=1" -gr 1 -hide 0,1,1,0 -fn figure1c_top
plopm -i figure1/METHOD_PYCOPM -v 'fluxnum - 1' -s ,3, -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Dual (vertical TF) $\Omega_\epsilon^{*,non-net}$, j=3" -gr 1 -hide 0,0,1,0 -fn figure1c_bottom
plopm -i figure1/METHOD_PYCOPM -v 'fluxnum - 1' -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Dual (no vertical TF) $\Omega_\epsilon^{*,net}$, j=1" -gr 1 -hide 0,1,1,0 -fn figure1d_top
plopm -i figure1/METHOD_PYCOPM -v 'fluxnum - 1' -s ,3, -xnt 5 -ynt 5 -ge black,1e-2 -cbl 'Net 0, non-net 1' -fz 16 -t "Dual (no vertical TF) c $\Omega_\epsilon^{*,non-net}$, j=3" -gr 1 -hide 0,0,1,0 -fn figure1d_bottom
