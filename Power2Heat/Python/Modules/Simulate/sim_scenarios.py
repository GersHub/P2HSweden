# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:34:08 2016

@author: Jonatan
"""

from __future__ import division
from sim_p2h import temp_to_heat, power_scen_to_res, sim_p2h

#scen = [0, 1, 2, 3, 4]
#scen = ['Current', 'Conservative', 'High RES', 'High RES & Surplus', 
#        'Extreme RES']
scen = ['Current', 'Conservative', 'High Wind',
        'High Wind & Solar']

cc, dhd = temp_to_heat()

for s in scen:
    P_res = power_scen_to_res(s)
    result = sim_p2h(P_res, cc, dhd, s)