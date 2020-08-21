# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:48:59 2016

@author: Jonatan
"""

from __future__ import division
from Modules.Plot.plot_results import plot_compare_scenarios
import os
import numpy as np

dir_Analysis = os.path.dirname(os.path.abspath(__file__))    
dir_Modules = os.path.dirname(dir_Analysis)

scen = ['Conservative', 'High Wind', 'High Wind & Solar']

for s in scen:
    def_min = 140
    
    power_cons = [125, def_min, 170]
    
    # stor p2h in a dictionary with tuples as keys
    p2h = {}
    p2h_tot = {}
    
    print 'Scenario {}'.format(s)
    for p in power_cons:
    
        print 'Power consumption : {}'.format(p)
        if p == def_min:
            filename = 'Scen_{}'.format(s)
        else:
            filename = 'Scen_{}_power_cons_{}'.format(s, p)
        file_location = os.path.join(dir_Modules, 'Results', 'p2h', 
                                     filename)
        result = np.loadtxt(file_location)
        p2h_tot[p] = np.sum(result)
        print 'P2H: {}'.format(np.sum(result))
        p2h['Consumption {} TWh.format(p)] = result
            
    plot_compare_scenarios(p2h, 'Scen_{}_power_cons'.format(s))
    
    
    for i in [125, 170]:
        percent_less = abs(p2h_tot[def_min] - p2h_tot[i])/p2h_tot[def_min] * 100
        print '{} percent change for {}'.format(percent_less, i)