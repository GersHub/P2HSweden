# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:50:51 2016

@author: Jonatan

Goal: Construct a case where you would have liked to take heat from both
        accumulators if it was available, but because of the regional
        restrictions, you only take heat from the one relevant
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from Modules.Accumulation.simulation import sim
from Modules.Plot.plot_ac import plot_compare_p2h

def test_regional_constraint():

    # make up demand data for two DH networks
    q_dict = {'lund':     np.array([3, 6, 7, 3, 0, 0, 0, 9, 3, 4]),
              'umea':   np.array([1, 0, 0, 0, 20, 20, 25, 6, 2, 4])}
    
    # make up power data
    P_res = 5 + np.array([8, 5, 7, 2, 1, 4, 0, 4, 7, 4])
                
    result = sim(q_dict, P_res)
    p2h = result['p2h']
    storage = result['storage']
    acs = result['acs']

    for index, q in enumerate(q_dict['lund']):
        # find a situation where the regional constraint comes into effect
        # first calculate maximal transfer from lund's accumulator
        max_transfer = {}
        for key in q_dict:
            max_transfer[key] = min(storage[key][index] - acs[key].min_storage, 
                                       acs[key].max_transfer)
        
        if  q_dict['umea'][index] > max_transfer['umea'] and \
            max_transfer['lund'] > q:
            if storage['lund'][index + 1] - storage['lund'][index] == q:
                return True
            else:
                return False   
            
    
#    for key, value in acs.iteritems():
#        print key,  'accumulator has storage capacity', value.max_storage, \
#                    'GWh and transfer capacity', value.max_transfer, 'GW'
#                    
#    plt.plot(1)
#    plt.clf()
#    for key, value in storage.iteritems():
#        plt.plot(value/acs[key].max_storage, label = key)
#    plt.legend()
#    plt.ylabel('Storage [%]')
#    plt.xlabel('Time [h]')
#    plt.ylim(0, 1)
#    
#    p2h_no_ac = np.minimum(sum(q_dict[key] for key in q_dict), P_res)
#    
#    #plot_compare_p2h(p2h_no_ac, p2h)
#    
#    plt.figure(10)
#    umea, = plt.plot(storage['umea'], label = 'umea')
#    lund, = plt.plot(storage['lund'], label = 'lund')
#    plt.legend(handles = [lund, umea])
#    plt.xlabel('Time [h]')
#    plt.ylabel('Storage [GWh]')

    return False
                
            
        
        

