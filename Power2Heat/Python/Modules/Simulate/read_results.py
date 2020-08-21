# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:39:40 2016

@author: Jonatan
"""

from __future__ import division
import os
import numpy as np

dir_Analysis = os.path.dirname(os.path.abspath(__file__))    
dir_Modules = os.path.dirname(dir_Analysis)

def read_results(scenario):
    """Returns the calculated hourly P2H potential
    for the given scenario."""
    
    if type(scenario) == int:
        filename = 'Scen_{}_size_1_transfer_1'.format(scenario)
    else:
        filename = scenario

    file_location = os.path.join(dir_Modules, 'Results', 'p2h_with_ac', 
                                 filename)        
    return np.loadtxt(file_location)
