# -*- coding: utf-8 -*-
"""
Created on Fri May 06 09:02:01 2016

@author: Jonatan
"""

from __future__ import division
import os
import numpy as np
from Modules.Plot.plot_results import plot_compare_scenarios


dir_Cost = os.path.dirname(os.path.abspath(__file__))
dir_Modules = os.path.dirname(dir_Cost)
dir_p2h = os.path.join(dir_Modules, 'Results', 'p2h')

#scenarios = [1, 2, 3, 4]
scenarios = ['Conservative', 'High Wind', 'High Wind & Solar']

for s in scenarios:
    
    # store results in a dict
    p2h = {}
    
    file_name = os.path.join(dir_p2h, 'Scen_{}_cost_opt'.format(s))
    # load the economical p2h potential
    p2h_ec = np.loadtxt(file_name)
    file_name = os.path.join(dir_p2h, 'Scen_{}'.format(s))
    p2h['base_case_ {}'.format(s)] = np.loadtxt(file_name)    
    
    print 'Scenario_{}'.format(s)
    print 'Total economical potential', np.sum(p2h_ec)/1000, 'TWh'
    print 'Capacity', max(p2h_ec), 'GW'

    p2h['cost_opt_{}'.format(s)] = p2h_ec

    plot_compare_scenarios(p2h, 'Scen_{}_cost'.format(s))
    
    