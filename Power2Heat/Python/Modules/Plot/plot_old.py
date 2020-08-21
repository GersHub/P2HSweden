# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:50:30 2016

@author: Jonatan
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from plot_results import plot_compare_sup_dem
from plot_ac import plot_compare_p2ac, plot_storage

def plot_results_old(result_dict):
    """ Performs a bunch of plots and prints results based on the simulation
    results.
    """
    county_curves = result_dict['county_curves']
    P_res = result_dict['P_res']
    # demand_pot refers to the hourly demand of heat that can potentially be
    # covered by P2H, taking into account a limited P2H capacity
    demand_pot = result_dict['demand_pot']
    # P_demand then refers to the hourly demand of electricity that is
    # needed to fulfull the demand_pot
    # Notice that when electric boiler are used with an efficiency of 1, 
    # P_demand is equal to demand_pot
    P_demand = result_dict['P_demand']
    p2h = result_dict['p2h']
    p2ac = result_dict['p2ac']
    P_surplus = result_dict['P_surplus']
    storage = result_dict['storage']
  
    # sum up the heat curves for all counties in order to get a total heat 
    # curve for the whole country
    q_tot = sum(county_curves.values())  
    
    # again sum up county values to get a value for the whole country
    tot_dem_pot = sum(demand_pot.values())
    
    #plot comparison between power data and DH data    
    plot_compare_sup_dem(P_res, q_tot, 'Heat Demand [GWh_th]', 12)    
    
    # plot the demand considering the limited P2H conversion, 
    # to compare with the actual DH heat demand
    plt.plot(tot_dem_pot, P_res, 'b.')
    
    # again sum up county values to get a value for the whole country
    tot_P_dem = sum(P_demand.values())
    
    # do the same for the demanded electrical power (with no heat
    # pumps but only electric boiler, this will be equal to the
    # tot_dem_pot)
    plot_compare_sup_dem(P_res, tot_P_dem, 'Power demand potential [GWh_el]', 
                         13, True)       
    
    # calculate power that cannot be harvested without accumulation,
    # i.e. the accumulation potential
    ac_pot = []
    
        
    for i, P in enumerate(P_surplus):
        if P> tot_P_dem[i]:
            ac_pot.append(P - tot_P_dem[i])
        else:
            ac_pot.append(0)
    
    print 'accumulation potential is', np.sum(ac_pot), 'GWh'
    
    if storage != 0:
        plot_storage(storage)
    
    # compare the theoretical accumulation potential to the technical
    # potential
    plot_compare_p2ac(ac_pot, p2ac)
    
    print 'Total accumulated heat', np.sum(p2ac), 'GWh'
        
    # print the total potential with accumulation
    print 'Total potential with accumulation:', np.sum(p2h), 'GWh'  
        
    