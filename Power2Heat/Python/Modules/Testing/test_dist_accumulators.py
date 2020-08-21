# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 09:23:37 2016

@author: Jonatan

Goal: Show that under certain conditions it is equivalent to work with one
central accumulator and to work with separate accumulators for each network.
The condition is that:
1) the different networks have hourly demand with same shape (for example
since they come from the same temperature profile), only normated by a factor
proportional to the total yearly load
2) the power residual is distributed proportionally to total yearly load
3) the accumulators are sized proportionally to total yearly load
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from test_accumulator import test_ac

def test_dist_ac():

    q_hourly_tot =  np.array([4, 6, 5, 6, 0, 8, 3, 5, 8, 2, 1, 5, 7])
    P_res =     np.array([4, 8, 3, 9, 5, 6, 8, 1, 0, 6, 3, 5, 9])
    
    q_tot = np.sum(q_hourly_tot)
    
    q_shares = [0.3, 0.5, 0.2]
    q_tot_dist = [i * q_tot for i in q_shares]
    
    # nominal trajectory
    q_nom_hourly = q_hourly_tot/q_tot
    
    # now we have the total demand for each network and a nominal trajectory
    # next step is to calculate actual trajectory for each network
    
    q_hourly_list = [i * q_nom_hourly for i in q_tot_dist]
    q_means = [np.mean(i) for i in q_hourly_list]
    
    # create a vector in which to store hourly data for the heat that is added
    # to DH networks (including additions to accumulators)
    p2h = [[] for i in q_shares]
    waste = [[] for i in q_shares]
    storage = [[] for i in q_shares]
    my_acs = [0 for i in q_shares]
    
    for i, ac in enumerate(my_acs):
        res = test_ac(q_hourly_list[i], P_res * q_tot_dist[i]/q_tot)
        p2h[i], waste[i], my_acs[i], storage[i] = res['p2h'], \
                                        res['waste'], res['ac'], res['storage']
    
    p2h_dist = (np.sum(p2h, 0)).astype(int)
    
    # get a list of lists with the history for each accumulator
    # there is some problem with the instance variable ac.history
    
    #acs_history = [ac.history for ac in my_acs]
    #my_acs_tot = np.sum(acs_history)
    storage_tot = np.sum(storage, 0)
    
    # simulate for central accumulator
    res = test_ac(q_hourly_tot, P_res)
    p2h_central, waste_central, my_ac_central, storage_central = res['p2h'], \
                                        res['waste'], res['ac'], res['storage']
                                        
    #print storage_tot - storage_central

    # compare p2h potential for the simulations with distributed and central
    # accumulators
    #plt.figure(2)
    #plt.clf()
    #dist, = plt.plot(p2h_dist, label = 'dist total')
    #central, = plt.plot(p2h_central, label = 'central')
    #dist_stor, = plt.plot(my_acs_tot, label = 'storage dist')
    #central_stor, = plt.plot(storage_central, label = 'storage central')
    #plt.legend(handles = [dist, central, dist_stor, central_stor])
    
    #plt.figure(3)
    #plt.clf()
    #for ac in my_acs:
    #    plt.plot(ac.history)
    
    #plt.figure(1)
    #for result in p2h:
    #    plt.plot(result)

    if  np.array_equal(p2h_dist, p2h_central) and \
        np.allclose(storage_tot, storage_central):
        return True
    else:
        return False        
    
        