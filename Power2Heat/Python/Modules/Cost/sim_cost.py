# -*- coding: utf-8 -*-
"""
Created on Wed May 04 09:01:24 2016

@author: Jonatan

Compare economical and technical potential
"""

from __future__ import division
from Modules.Simulate.sim_p2h import temp_to_heat, power_scen_to_res, sim_p2h
from cost_opt import optimize_capacity, calc_profit
import numpy as np

#scen = [1, 2, 3, 4]
scen = ['Conservative', 'High Wind', 'High Wind & Solar']

cc, dh = temp_to_heat()

# calculate total design_heat_capacity
dh_tot = sum(dh.values())    

# initialize share and profit to zero
share_old = 0
profit_old = 0

for s in scen:
    P_res = power_scen_to_res(s)
    
    # optimize the p2h capacity with respect to costs
    p2h_capacity = optimize_capacity(s)
    
    # assume the electric boilers are distributed evenly over the
    # regions
    share_new = p2h_capacity/dh_tot
    
    # for share_upper we need to simulate and calculate the profit
    results = sim_p2h(P_res, cc, dh, s, p2h_share = share_new)
    
    # extract the p2h potential
    q_heat = np.sum(results['p2h'])
    
    # calculate the profit
    result = calc_profit(p2h_capacity, q_heat)    
    profit_new = result['profit']
    
    print 'Capacity', share_new
    print 'Profit', profit_new, 'MSEK'
    
    # improve the optimization
    # so far the result gives to high profit
    # therefore the optimal investment will be somewhat lower
    # we test with lower values as long as the profit increases
    
    stepsize = 0.0001

    while np.absolute(profit_new > profit_old):
        
        share_old = share_new
        profit_old = profit_new
        
        # split the interval in two and solve for the value in the middle
        share_new = share_old - stepsize
    
        # simulate p2h
        results = sim_p2h(P_res, cc, dh, s, p2h_share = share_new)
        
        # now extract the actual p2h potential
        q_heat = np.sum(results['p2h'])
        
        # calculate the profit based on this
        result = calc_profit(share_new * dh_tot, q_heat)
        
        profit_new = result['profit']
        print 'Capacity', share_new
        print 'Profit', profit_new, 'MSEK'
        
    # the optimal share is share_old
    print 'The optimal share is', share_old, 'of design heat load'
        
    print 'The actual profit is', profit_old, 'MSEK'