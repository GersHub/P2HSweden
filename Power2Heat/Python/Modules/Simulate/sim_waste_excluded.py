# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 11:05:27 2016

@author: Jonatan
"""

from __future__ import division
from sim_p2h import sim_p2h, power_scen_to_res, temp_to_heat

#scen = [1, 2, 3, 4]
scen = ['Conservative', 'High Wind', 'High Wind & Solar']

exclude_waste = [True, False]

P_res = {}

for s in scen:
    P_res[s] = power_scen_to_res(s) 

for e in exclude_waste:
    cc, dhd = temp_to_heat(e)
    for s in scen:
        sim_p2h(P_res[s], cc, dhd, s, e)