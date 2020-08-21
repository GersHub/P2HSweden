# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:50:51 2016

@author: Jonatan

Goal: Test strategy for accumulators
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from Modules.Accumulation.simulation import sim
from Modules.Plot.plot_ac import plot_compare_p2h

def test_acs_priority():

    # make up demand data for two DH networks
    q_dict = {'lund':     np.array([3, 6, 7, 8, 2, 5, 7, 9, 3, 4]),
              'umea':   np.array([1, 0, 5, 8, 3, 9, 4, 6, 2, 4])}
    
    # make up power data
    P_res = 5 + np.array([8, 5, 7, 2, 1, 4, 0, 4, 7, 4])
                
    result = sim(q_dict, P_res)
    p2h = result['p2h']
    storage = result['storage']
    acs = result['acs']
    
    # test if a gap between the relative storages of two accumulators can
    # increase from one time step to the next
    
    old_gap = 0   
    
    for index, value in enumerate(storage['lund']):
        new_gap = value/acs['lund'].max_storage - \
                storage['umea'][index]/acs['umea'].max_storage
        
        if old_gap> 0 and new_gap > old_gap:
            return False
        elif old_gap < 0 and new_gap < old_gap:
            return False
                
    #plt.plot(1)
    #plt.clf()
    #for key, value in storage.iteritems():
    #    plt.plot(value/np.mean(q_dict[key])/24, label = key)
    #plt.legend()
    #plt.ylabel('Storage [%]')
    #plt.xlabel('Time [h]')
    #    
    #p2h_no_ac = np.minimum(sum(q_dict[key] for key in q_dict), P_res)
    #
    #plot_compare_p2h(p2h_no_ac, p2h)
    #
    #plt.figure(10)
    #umea, = plt.plot(storage['umea'], label = 'umea')
    #lund, = plt.plot(storage['lund'], label = 'lund')
    #plt.legend(handles = [lund, umea])
    #plt.xlabel('Time [h]')
    #plt.ylabel('Storage [GWh]')
                
    return True
                
            
        
        

