# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:30:09 2016

@author: Jonatan
"""

from __future__ import division
from Modules.Accumulation.Accumulator import Accumulator
from Modules.Accumulation.simulation import sim_ac
import numpy as np

def test_zero_ac():

    P_surplus = [0, 0, 4, 5, 6, 0, 0, 2, 8, 5, 7, 0, 0, 0, 0, 3, 4, 5, 8, 1, 0]
    
    Q_demand = {'stockholm': 
                [3, 5, 6, 2, 3, 1, 3, 5, 2, 4, 1, 3, 1, 3, 4, 1, 3, 5, 1, 3, 3]}
                
    # find potential without accumulation
    p2h = np.minimum(P_surplus, Q_demand['stockholm'])
    
    #print 'p2h', np.sum(p2h)
    
    acs = {'stockholm': Accumulator(0, 0, 0, 0)}
    
    results = sim_ac(Q_demand, P_surplus, acs)
    
    p2h_ac = results['p2h']
    
    #print 'p2h_ac', np.sum(p2h_ac)
    
    if np.sum(p2h) == np.sum(p2h_ac):
        return True
    else:
        return False