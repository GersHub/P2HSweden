# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:39:40 2016

@author: Jonatan
"""

from __future__ import division
from Modules.Plot.plot_results import plot_compare_scenarios
import os
import numpy as np
import matplotlib.pyplot as plt

dir_Analysis = os.path.dirname(os.path.abspath(__file__))    
dir_Modules = os.path.dirname(dir_Analysis)

def read_results():
    """Returns a dictionary containing the calculated hourly P2H potential
    for the given scenarios."""
    
    p2h = {}
    
    #scenarios = [0, 1, 2, 3, 4]
#    scenarios = ['Current', 'Conservative', 'High RES', 'High RES & Surplus', 
#        'Extreme RES']
#    scenarios = ['Current', 'Conservative', 'Low Consumption', 'High Wind',
#        'High Wind, High Solar']
    scenarios = ['Current', 'Conservative', 'High Wind',
            'High Wind & Solar']
    
    for s in scenarios:
        file_location = os.path.join(dir_Modules, 'Results', 'p2h', 'Scen_{}'.format(s))
        p2h[s] = np.loadtxt(file_location)
        print 'Potential for Scenario', s, ':', sum(p2h[s])
        
    return p2h
    
if __name__ == '__main__':
    
    # read results
    p2h = read_results()
    
    # plot comparison        
    plot_compare_scenarios(p2h, 'Scenarios')
    
#    # work now with the results for the High Wind scenario
#    p = p2h['High Wind']
#    
#    peak_ind = np.nonzero(p)[0]
#    
#    # declare a variable used to count the number of peaks
#    peak_counter = 0   
#    
#    # store the previous peak index
#    previous_ind = -2
#    
#    for i in peak_ind:
#        if i - previous_ind > 1:
#            # then there was a zero value in between
#            # thus add to the peak counter
#            peak_counter += 1
#        previous_ind = i
#    
#    print 'Number of peaks is:', peak_counter
#    
#    plt.figure(3)
#    plt.plot(p)
