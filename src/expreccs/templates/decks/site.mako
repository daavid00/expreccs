<%
import math as mt
import numpy as np
%>
-- Copyright (C) 2023 NORCE
----------------------------------------------------------------------------
RUNSPEC
----------------------------------------------------------------------------
DIMENS 
${dic['site_noCells'][0]} ${dic['site_noCells'][1]} ${dic['site_noCells'][2]} /

EQLDIMS
/

TABDIMS
${dic['satnum']} 1* 10000 /

OIL
GAS
CO2STORE

METRIC

START
1 'JAN' 2025 /

WELLDIMS
${len(dic['site_wellijk'])} ${dic['site_noCells'][2]} ${len(dic['site_wellijk'])} ${len(dic['site_wellijk'])} /

UNIFIN
UNIFOUT

%if dic['site_bctype'] == 'flux':
AQUDIMS
-- MXNAQN   MXNAQC   NIFTBL  NRIFTB   NANAQU    NNCAMAX
    1*       1*        5       100      ${len(dic['AQUFLUX_top'][0][0])+len(dic['AQUFLUX_bottom'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_left'][0][0])}         1000 /
% endif
----------------------------------------------------------------------------
GRID
----------------------------------------------------------------------------
INCLUDE
'GEOLOGY_${reservoir.upper()}.INC' /

%if dic['site_bctype'] == 'flux':
BCCON
${1+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])+len(dic['AQUFLUX_top'][0][0])} 1 1 1 1 1 1 J- /
/
%elif dic['site_bctype'] == 'pres':
BCCON
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["site_noCells"][1]):
${i+1+k*dic["site_noCells"][1]} 1  1  ${i+1} ${i+1} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}    'I-'  /
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["site_noCells"][1]):
${i+1+k*dic["site_noCells"][1]+dic['regional_noCells'][2]*dic["site_noCells"][1]} ${dic['site_noCells'][0]}  ${dic['site_noCells'][0]}  ${i+1} ${i+1} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}  'I'  /
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["site_noCells"][0]):
${i+1+k*dic["site_noCells"][0]+2*dic['regional_noCells'][2]*dic["site_noCells"][1]} ${i+1} ${i+1} 1 1 ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1} 'J-'  /
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["site_noCells"][0]):
${i+1+k*dic["site_noCells"][0]+2*dic['regional_noCells'][2]*dic["site_noCells"][1]+dic['regional_noCells'][2]*dic["site_noCells"][0]} ${i+1} ${i+1} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1} 'J'   /
% endfor
% endfor
/
%elif dic['site_bctype'] == 'free':
BCCON
1 1 ${dic['site_noCells'][0]} 1 1 1* 1* Y- /
2 1 ${dic['site_noCells'][0]} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} 1* 1* Y /
3 1 1 1 ${dic['site_noCells'][1]} 1* 1* X- /
4 ${dic['site_noCells'][0]} ${dic['site_noCells'][0]} 1 ${dic['site_noCells'][1]} 1* 1* X /
/
%elif dic['site_bctype'] == 'porv':
----------------------------------------------------------------------------
EDIT
----------------------------------------------------------------------------
BOX
1 1 1 ${dic['site_noCells'][0]} 1* 1* / 
MULTPV
% for _ in range(dic['site_noCells'][2]):
% for i in range(dic['site_noCells'][0]):
${'\t\t{0:.15e}'.format(dic["site_porv"]) }\
% endfor
${'/\n' if loop.last else ' '}\
% endfor
ENDBOX

BOX
1 ${dic['site_noCells'][0]} 1 1 1* 1* / 
MULTPV
% for _ in range(dic['site_noCells'][2]):
% for i in range(dic['site_noCells'][0]):
${'\t\t{0:.15e}'.format(dic["site_porv"]) }\
% endfor
${'/\n' if loop.last else ' '}\
% endfor
ENDBOX

BOX
${dic['site_noCells'][1]} ${dic['site_noCells'][1]} 1 ${dic['site_noCells'][0]} 1* 1* / 
MULTPV
% for _ in range(dic['site_noCells'][2]):
% for i in range(dic['site_noCells'][0]):
${'\t\t{0:.15e}'.format(dic["site_porv"]) }\
% endfor
${'/\n' if loop.last else ' '}\
% endfor
ENDBOX

BOX
1 ${dic['site_noCells'][0]} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} 1* 1* / 
MULTPV
% for _ in range(dic['site_noCells'][2]):
% for i in range(dic['site_noCells'][0]):
${'\t\t{0:.15e}'.format(dic["site_porv"]) }\
% endfor
${'/\n' if loop.last else ' '}\
% endfor
ENDBOX
%endif
----------------------------------------------------------------------------
PROPS
----------------------------------------------------------------------------
INCLUDE
'PROPS_${reservoir.upper()}.INC' /
----------------------------------------------------------------------------
REGIONS
----------------------------------------------------------------------------
INCLUDE
'REGIONS_${reservoir.upper()}.INC' /
----------------------------------------------------------------------------
SOLUTION
---------------------------------------------------------------------------
EQUIL
 0 ${dic['pressure']} 1000 0 0 0 1 1 0 /

RTEMPVD
0   ${dic['temp_top']}
${dic[f'{reservoir}_zmz'][-1]} ${dic['temp_bottom']} /

RPTRST 
 'BASIC=2' FLOWS FLORES DEN/

%if dic['site_bctype'] == 'flux': 
AQUANCON
-- Aq#  I1 I2  J1   J2  K1 K2 FACE
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["left_noCells"]):
${i+1+k*dic["left_noCells"]} 1  1  ${1+i*mt.floor(dic['site_noCells'][1]/dic["left_noCells"])} ${(i+1)*mt.floor(dic['site_noCells'][1]/dic["left_noCells"])} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'I-'	  1.00      1  /
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["right_noCells"]):
${i+1+k*dic["right_noCells"]+len(dic['AQUFLUX_left'][0][0])} ${dic['site_noCells'][0]}  ${dic['site_noCells'][0]}  ${1+i*mt.floor(dic['site_noCells'][1]/dic["right_noCells"])} ${(i+1)*mt.floor(dic['site_noCells'][1]/dic["right_noCells"])} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'I'	  1.00      1  /
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["bottom_noCells"]):
% if ((i+1)*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"]) != 1 and 1+i*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])!=dic['site_noCells'][0]) and dic["bottom_noCells"]>2:
% if i==0:
${i+1+k*dic["bottom_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])} ${2} ${(i+1)*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])} 1 1 ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J-'	  1.00      1  /
% elif i==dic["bottom_noCells"]-1:
${i+1+k*dic["bottom_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])} ${1+i*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])} ${dic['site_noCells'][0]-1} 1 1 ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J-'	  1.00      1  /
%else:
${i+1+k*dic["bottom_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])} ${1+i*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])} ${(i+1)*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])} 1 1 ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J-'	  1.00      1  /
% endif
% endif
% endfor
% endfor
% for k in range(dic['regional_noCells'][2]):
% for i in range(dic["top_noCells"]):
% if ((i+1)*mt.floor(dic['site_noCells'][0]/dic["top_noCells"]) != 1 and 1+i*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])!=dic['site_noCells'][0]) and dic["top_noCells"]>2:
% if i==0:
${i+1+k*dic["top_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])} ${2} ${(i+1)*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J'	  1.00      1  /
% elif i==dic["top_noCells"]-1:
${i+1+k*dic["top_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])} ${1+i*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])} ${dic['site_noCells'][0]-1} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J'	  1.00      1  /
%else:
${i+1+k*dic["top_noCells"]+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])} ${1+i*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])} ${(i+1)*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])} ${dic['site_noCells'][1]} ${dic['site_noCells'][1]} ${np.where(dic["site_zmaps"]==k)[0][0]+1} ${np.where(dic["site_zmaps"]==k)[0][-1]+1}	'J'	  1.00      1  /
% endif
% endif
% endfor
% endfor
/
%endif
----------------------------------------------------------------------------
SUMMARY
----------------------------------------------------------------------------
FPR
FGIP
FOIP
FGIR
FGIT
WGIR
/
WOIR
/
WGIT
/
WBHP
/
RPR
/
ROIP
/
RGIP
/
----------------------------------------------------------------------------
SCHEDULE
----------------------------------------------------------------------------
RPTRST
 'BASIC=2' FLOWS FLORES DEN /

WELSPECS
% for i in range(len(dic['site_wellijk'])):
	'INJ${i}'	'G1'	${dic['site_wellijk'][i][0]}	${dic['site_wellijk'][i][1]}	1*	'GAS' /
% endfor
/
COMPDAT
% for i in range(len(dic['site_wellijk'])):
	'INJ${i}'	${dic['site_wellijk'][i][0]}	${dic['site_wellijk'][i][1]}	${dic['site_wellijk'][i][2]}	${dic['site_wellijk'][i][3]}	'OPEN'	1*	1*	0.5 /
% endfor
/
% for j in range(len(dic['inj'])):
TUNING
${min(1, dic['inj'][j][2])} ${dic['inj'][j][2]} 1e-10 2* 1e-12/
/
/
WCONINJE
% for i in range(len(dic['site_wellijk'])):
% if dic['inj'][j][3+2*i] > 0:
'INJ${i}' 'GAS' ${'OPEN' if dic['inj'][j][2*(i+2)] > 0 else 'SHUT'}
'RATE' ${f"{dic['inj'][j][2*(i+2)] / 1.86843 : E}"}  1* 400/
% else:
'INJ${i}' 'OIL' ${'OPEN' if dic['inj'][j][2*(i+2)] > 0 else 'SHUT'}
'RATE' ${f"{dic['inj'][j][2*(i+2)] / 998.108 : E}"}  1* 400/
%endif
% endfor
/
%if dic['site_bctype'] == 'flux':
AQUFLUX
% for i in range(len(dic['AQUFLUX_left'][0][0])):
${i+1} ${dic['AQUFLUX_left'][j+1][0][i]} /
% endfor
% for i in range(len(dic['AQUFLUX_right'][0][0])):
${i+1+len(dic['AQUFLUX_left'][0][0])} ${dic['AQUFLUX_right'][j+1][0][i]} / 
% endfor
% for i in range(len(dic['AQUFLUX_bottom'][0][0])):
% if ((i%dic["bottom_noCells"]+1)*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"]) != 1 and 1+(i%dic["bottom_noCells"])*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])!=dic['site_noCells'][0]) and dic["bottom_noCells"]>2:
${i+1+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])} ${dic['AQUFLUX_bottom'][j+1][0][i]} /
% endif
% endfor
% for i in range(len(dic['AQUFLUX_top'][0][0])):
% if ((i%dic["top_noCells"]+1)*mt.floor(dic['site_noCells'][0]/dic["top_noCells"]) != 1 and 1+(i%dic["top_noCells"])*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])!=dic['site_noCells'][0]) and dic["top_noCells"]>2:
${i+1+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])} ${dic['AQUFLUX_top'][j+1][0][i]} /
% endif
% endfor
/
BCPROP
${1+len(dic['AQUFLUX_left'][0][0])+len(dic['AQUFLUX_right'][0][0])+len(dic['AQUFLUX_bottom'][0][0])+len(dic['AQUFLUX_top'][0][0])} DIRICHLET OIL 1* ${dic['PRESSURE_bottom'][j+1][0][0]} /
/
%elif dic['site_bctype']== 'pres':
BCPROP
% for i in range(len(dic['PRESSURE_left'][0][0])):
${i+1} DIRICHLET OIL 1* ${dic['PRESSURE_left'][j+1][0][i]} /
% endfor
% for i in range(len(dic['PRESSURE_right'][0][0])):
${i+1+len(dic['PRESSURE_left'][0][0])} DIRICHLET OIL 1* ${dic['PRESSURE_right'][j+1][0][i]} / 
% endfor
% for i in range(len(dic['PRESSURE_bottom'][0][0])):
% if ((i%dic["bottom_noCells"]+1)*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"]) != 1 and 1+(i%dic["bottom_noCells"])*mt.floor(dic['site_noCells'][0]/dic["bottom_noCells"])!=dic['site_noCells'][0]) and dic["bottom_noCells"]>2:
${i+1+len(dic['PRESSURE_left'][0][0])+len(dic['PRESSURE_right'][0][0])} DIRICHLET OIL 1* ${dic['PRESSURE_bottom'][j+1][0][i]} /
% endif
% endfor
% for i in range(len(dic['PRESSURE_top'][0][0])):
% if ((i%dic["top_noCells"]+1)*mt.floor(dic['site_noCells'][0]/dic["top_noCells"]) != 1 and 1+(i%dic["top_noCells"])*mt.floor(dic['site_noCells'][0]/dic["top_noCells"])!=dic['site_noCells'][0]) and dic["top_noCells"]>2:
${i+1+len(dic['PRESSURE_left'][0][0])+len(dic['PRESSURE_right'][0][0])+len(dic['PRESSURE_bottom'][0][0])} DIRICHLET OIL 1* ${dic['PRESSURE_top'][j+1][0][i]} /
% endif
% endfor
/
%elif dic['site_bctype'] == "free":
BCPROP 
1 FREE /
2 FREE /
3 FREE /
4 FREE /
/
%endif
TSTEP
${mt.floor(dic['inj'][j][0]/dic['inj'][j][1])}*${dic['inj'][j][1]}
/
% endfor