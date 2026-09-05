flow FIGURE2.DATA --relaxed-max-pv-fraction=0 --enable-tuning=true --enable-dry-run=1 --output-dir=figure2
plopm -i figure2/FIGURE2 -v 'fluxnum - 1' -ge 'black,1e-2' -cbl 'Net 0, non-net 1' -fz 8 -fn figure2 -hide 0,0,0,1
