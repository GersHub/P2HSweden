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

#s = 4
scen = ['Conservative', 'High Wind', 'High Wind & Solar']

for s in scen:
    print 'Scenario {}'.format(s)
    
    p2h = {}
    
    file_location = os.path.join(dir_Modules, 'Results', 'p2h', 'Scen_{}'.format(s))
    result = np.loadtxt(file_location)
    p2h_inc_tot = np.sum(result)
    print 'P2H including waste: {}'.format(p2h_inc_tot)
    p2h['including_waste'] = result
    
    file_location = os.path.join(dir_Modules, 'Results', 'p2h', 'Scen_{}_ex_waste'.format(s))
    result = np.loadtxt(file_location)
    p2h_ex_tot =np.sum(result)
    print 'P2H excluding waste: {}'.format(p2h_ex_tot)
    p2h['excluding_waste'] = result
            
    plot_compare_scenarios(p2h, 'Scen_{}_waste'.format(s))
    
    percent_less = (p2h_inc_tot - p2h_ex_tot)/p2h_inc_tot * 100
    print '{} percent less when waste is excluded'.format(percent_less)