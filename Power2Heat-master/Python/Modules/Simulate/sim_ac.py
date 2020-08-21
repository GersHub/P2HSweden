# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:39:28 2016

@author: Jonatan

Compare results for different accumulator sizes

"""

from __future__ import division
from sim_p2h import sim_p2h, power_scen_to_res, temp_to_heat

#scen = [1, 2, 3, 4]
scen = ['Conservative', 'High Wind', 'High Wind & Solar']

ac_sizes = [1, 10]

P_res = {}

cc, dhd = temp_to_heat(exclude_waste = False)

for s in scen:
    P_res[s] = power_scen_to_res(s)    
    for a in ac_sizes:
        sim_p2h(P_res[s], cc, dhd, s, ac_size = a, ac_transfer = a)