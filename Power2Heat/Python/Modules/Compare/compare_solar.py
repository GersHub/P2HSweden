# -*- coding: utf-8 -*-
"""
Created on Fri May 13 15:30:12 2016

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
    solar_yr = [2011, 2012, 2013, 2014, 2015]
    
    # stor p2h in a dictionary with tuples as keys
    p2h = {}
    
    max_p2h = 0
    min_p2h = 10000
    
    print 'Scenario {}'.format(s)
    for y in solar_yr:
    
        print 'solar yr : {}'.format(y)
        if y == 2014:
            filename = 'Scen_{}'.format(s)
        else:
            filename = 'Scen_{}_solar_yr_{}'.format(s, y)
        file_location = os.path.join(dir_Modules, 'Results', 'p2h', 
                                     filename)
        result = np.loadtxt(file_location)
        if y == 2014:
            p2h_2014 = np.sum(result)
        
        print 'P2H: {}'.format(np.sum(result))
        p2h['solar_yr_{}'.format(y)] = result
            
    plot_compare_scenarios(p2h, 'Scen_{}_solar'.format(s))
    
    p2h_tot = {}
    
    for key, value in p2h.iteritems():
        p2h_tot[key] = np.sum(value)
    print ''
    print '2012:', p2h_tot['solar_yr_2012'], '({} % more than for 2014)'.format((p2h_tot['solar_yr_2012'] - p2h_2014)/p2h_2014 * 100)
    print '2011:', p2h_tot['solar_yr_2011'], '({} % less than for 2014)'.format((p2h_2014 - p2h_tot['solar_yr_2011'])/p2h_2014 *100)
    #print 'Mean:', np.mean(p2h_tot)