# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 09:23:37 2016

@author: Jonatan

Goal: implement one central accumulator which all networks can use (even if
this is not realistic)
"""

from __future__ import division
#from main_DH import main_DH
from Modules.Accumulation.Accumulator import Accumulator
import matplotlib.pyplot as plt
import numpy as np

def test_ac(q_hourly, P_res):    
    """ Simulates optimal use of an accumulator dimensioned proporsionally to
    the mean daily DH demand and returns the results.
    """  
    
    # model accumulator
    q_mean_daily = np.mean(q_hourly) * 24     
    my_ac = Accumulator(q_mean_daily, 0, q_mean_daily/12, q_mean_daily/2)
    
    # create a vector in which to store hourly data for the heat that is added
    # to DH networks (including additions to accumulators)
    p2h = []
    waste = []
    storage = []
    
    # implement priority list
    for i, p in enumerate(P_res):
        q = q_hourly[i]
        if q > p:
            # all power residual can be consumed directly
            p2h.append(p)
            my_ac.withdraw(q - p)
            waste.append(0)
        else:
            # store surplus energy in accumulator
            q_add = my_ac.add(p - q)
            waste.append(p - q - q_add)
            # we add q directly to the network and q_add to the storage tank 
            p2h.append(q + q_add)
        
        storage.append(my_ac.current_storage)
        
            
    return {'p2h': p2h,
            'waste': waste,
            'ac': my_ac,
            'storage': storage}

if __name__ == '__main__': 
            
    q_hourly =  np.array([4, 6, 5, 6, 0, 8, 3, 5, 8, 2, 1, 5, 7])
    P_res =     np.array([4, 8, 3, 9, 5, 6, 8, 1, 0, 6, 3, 5, 9])
        
    res = test_ac(q_hourly, P_res)
    p2h, waste, my_ac = res['p2h'], res['waste'], res['ac']
    
    # plot and interpret results
    plt.figure(1)
    q, = plt.plot(q_hourly, label = 'q_demand')
    p, = plt.plot(P_res, label = 'P_res')
    ac, = plt.plot(my_ac.history, label = 'Ac')
    w, = plt.plot(waste, label = 'wasted energy')
    plt.legend(handles = [q, p, ac, w])
    
    # compare p2h potential to the case without accumulator
    p2h_no_ac = np.minimum(q_hourly, P_res)
    plt.figure(2)
    with_ac, = plt.plot(p2h, label = 'with ac')
    no_ac, = plt.plot(p2h_no_ac, label = 'no_ac')
    plt.legend(handles = [with_ac, no_ac])
    
    plt.figure(3)
    waste_no_ac = np.maximum(P_res - q_hourly, 0)
    w_with, = plt.plot(waste, label = 'waste with ac')
    w_no, = plt.plot(waste_no_ac, label = 'waste without ac')
    plt.legend(handles = [w_with, w_no])


        
    
        