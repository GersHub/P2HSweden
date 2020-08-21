# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 09:13:25 2016

@author: Jonatan
"""

from __future__ import division
from sim_p2h import temp_to_heat, power_scen_to_res, sim_p2h

#scen = [1, 2, 3, 4]
scen = ['Conservative', 'High Wind', 'High Wind & Solar']

power_cons = [125, 170]

# first calculate heat curves
county_curves, design_heat_dict = temp_to_heat()

for s in scen:
    for p in power_cons:
        P_res = power_scen_to_res(s, power_cons = p)
        sim_p2h(P_res, county_curves, design_heat_dict, s, power_cons = p)