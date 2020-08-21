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

#scenarios = [1, 2, 3, 4]
scenarios = ['Conservative', 'High Wind', 'High Wind & Solar']

ac_sizes = [0, 1, 10]

# stor p2h in a dictionary with tuples as keys
p2h = {}

for s in scenarios:
    for a in ac_sizes:
        
        if a == 0:
            filename = 'Scen_{}'.format(s)
            key = 'No storage'      
        else:
            filename = 'Scen_{}_size_{}_transfer_{}'.format(s, a, a)
            if a == 1:
                key = 'Modest storage'
            else:
                key = 'Huge storage'
            
        file_location = os.path.join(dir_Modules, 'Results', 'p2h', filename)
            
        p2h[key] = np.loadtxt(file_location)
        print 'Ac size:', a, 'P2H potential:', sum(p2h[key])
    
    plot_compare_scenarios(p2h, 'Scen_{}_ac'.format(s))

    p2h_max = np.sum(p2h['Huge storage'])
    p2h_mod = np.sum(p2h['Modest storage'])
    p2h_no = np.sum(p2h['No storage'])
    
    percent_more = (p2h_max - p2h_no)/p2h_no * 100
    print'{} percent more huge accumulation tanks'.format(percent_more)
    
    percent_more = (p2h_mod - p2h_no)/p2h_no * 100
    print'{} percent more with modest accumulation tanks'.format(percent_more)