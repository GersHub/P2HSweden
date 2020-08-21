# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 11:53:40 2016

@author: Jonatan
"""

from __future__ import division
import numpy as np
from Accumulator import Accumulator
from Modules.Power.calc_power import p2h_ratio
    
def sim_ac(q_dict, P, acs):
    """ Reads a dictionary with regional heat demands, the hourly power
    residual and the regional accumulators, and calculates the
    hourly potential for P2H.
    """
    
    # first check to that available power is not negative
    for p in P:
        if p < 0:
            raise Exception('Cannot have negative amount of available power!')        
   
    # set up lists to store the results
    # let p2h store the power to heat for each hour
    p2h = [0 for p in P]
    # let p2ac store the power used to fill accumulators for each hour
    p2ac = [0 for p in P]
    storage = {}
    for key in q_dict:
        storage[key] = []
    
    # simulate   
    for t, p in enumerate(P):
                
        # first record the current storage
        for key, value in storage.iteritems():
            value.append(acs[key].current_storage)       
        
        # calculate the total heat demand for time t
        q = sum([q_dict[county][t] for county in q_dict])

        # calculate the difference between available heat (from converting
        # the available power) and the demanded heat
        surplus = p/p2h_ratio() - q
        # calculate the relative storages for the accumulators at time t
        rel_storages = [(key, acs[key].get_rel_storage()) for key in acs]
        # sort the list of accumulators according to relative storage
        rel_storages.sort(key=lambda tup: tup[1])
        
        # now first handle the case with excess energy
        if surplus > 0:
            # start by meeting the current DH demand q
            p2h[t] += q
            # now use the surplus to fill up the accumulators
            while surplus > 0 and rel_storages:
                lowest_stor = rel_storages[0]
                # if the lowest relative storage is 1, all accumulators are full
                if lowest_stor[1] == 1:
                    # in this case we end the loop
                    break
                else:
                    # otherwise we fill up the this accumulator as much as possible
                    q_added = acs[lowest_stor[0]].add(surplus)
                    # update the surplus
                    surplus -= q_added
                    # eliminate the filled up accumulator from the list
                    rel_storages.pop(0)
                    # count the heat added to the accumulator in the record of
                    # total p2h
                    p2ac[t] += q_added
                    p2h[t] += q_added
        
        # now handle the case where the power available is greater than the total
        # demand
        else:
            deficit = (-1) * surplus
            
            # in this case all the available power can be used to cover (as 
            # much as possible of the) current DH demand. But in order to 
            # know how to best distribute the power, we should start by
            # investigating which accumulators it is strategic to use.
            
            # For each region the accumulator is used to cover as 
            # much as possible of the remaining heat demand
            # in order to do this we have to work with the regional heat
            # demands

            while deficit > 0 and rel_storages:
                # Select the accumulator with the maximum relative storage
                # out of the ones that haven't been filled for this time 
                # step. Give it the temporary name max_stor
                max_stor = rel_storages[-1]
                # if this (maximal) storage is 0, all accumulators are empty
                if max_stor[1] == 0:
                    # in that case, break the loop
                    break
                else:
                    # otherwise we withdraw as much heat as possible from this
                    # region's heat demand, as long as there is still a dificit
                
                    # find the county holding the current accumulator
                    county = max_stor[0]
                    
                    # now find the minimum of the national deficit and the
                    # regional demand at this time
                    desired_heat = min(deficit, q_dict[county][t])
                    # of this heat we withdraw as much as possible
                    q_extracted = acs[max_stor[0]].withdraw(desired_heat)
                    # update the deficit
                    deficit -= q_extracted
                    # eliminate the accumulator used from the list
                    rel_storages.pop(-1)
                    
            # now that as much as possible of the deficit has been covered
            # by the accumulators, the available power is distributed to
            # over the regions to cover its share
            p2h[t] += p
        
    return {'p2h': p2h,
            'p2ac': p2ac,
            'storage': storage,
            'acs': acs}
            
def sim(q_dict, P, trans_limits = -1):
    """ Simulates accumulation when using p2h technology for a system of
        accumulators
    """
    
        # set up accumulators
    acs = {}
    for key, value in q_dict.iteritems():
        q_daily_mean = np.mean(value) * 24
        # if accumulator transfer limit is not specified, set it to a
        # standard value relative to q_daily_mean
        if trans_limits == -1:
            trans_lim = q_daily_mean/40
        else:
            trans_lim = trans_limits[key]
        acs[key] = Accumulator(q_daily_mean/4, 0, trans_lim, q_daily_mean/8)
    
    return sim_ac(q_dict, P, acs) 