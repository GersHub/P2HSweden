# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 16:05:55 2016

@author: Jonatan
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
import time

from Modules.Power.specify_scenarios import specify_scenario
from Modules.Power.calc_power import calc_power_curves, calc_power_residual, p2h_ratio
from Modules.Power.read_power_data import read_power_data

from Modules.DH.calc_county_curves import calc_county_curves
from Modules.DH.read_temp_data import read_temp_data
from Modules.DH.read_cities import read_cities

from Modules.Accumulation.simulation import sim_ac
from Modules.Accumulation.Accumulator import Accumulator
from Modules.Plot.plot_old import plot_results_old

def temp_to_heat(exclude_waste = False):
    """
    Read regional temperature data from file and calculate heat curves.
    """

    # read hourly temperature data and extreme temperature for all regions
    # key = county, value = {'T_ext', 'data_list'}
    temp_dict = read_temp_data() 
    
    # Read DH data and GIS data for Swedish cities, divide data into regions
    # key = city name, value = [county, q_tot]
    heat_dict = read_cities(exclude_waste)
    
    # now calculate heat curves and design heat loads for each region
    return calc_county_curves(temp_dict, heat_dict, exclude_waste)
    
def power_scen_to_res(scenario, hydro_min = 1.682,
                                solar_yr = 2014,
                                power_cons = -1):
    """ Calculate the hourly power residual based on the scenario.
    """
    
    # the scenario can be specified either by an int corresponding
    # to a standard scenario, or by providing a dictionary which
    # specifies the scenario
    if type(scenario) == dict:
        scenario_data = scenario
    elif type(scenario) == int or type(scenario) == str:           
        # import the scenario specification
        scenario_data = specify_scenario(scenario)
    else:
        raise Exception('Invalid scenario specification!')
        
    # if power consumption is varied, enter it into the scenario data here
    if power_cons >= 0:
        scenario_data["Consumption"] = power_cons
    
    # read the power data
    power_data = read_power_data()
    
    # calculate the power curves [GW]
    power_curves = calc_power_curves(scenario_data, power_data)
    
    # calculate curve for power residual [GW]
    return calc_power_residual(power_curves, hydro_min = hydro_min)
    
def sim_p2h(P_res, county_curves, design_heat_dict, scenario_nbr,
            exclude_waste = False, 
            ac_size = 0,
            ac_transfer = 0,
            hydro_min = -1,
            wind_yr = 2014,
            solar_yr = 2014,
            p2h_share = 0.3,
            power_cons = -1):
                
    """ Based on heat curves and power residual, simulate P2H.
    The result is printed to file but also returned in a dictionary.
    """     
    
    # calculate the regional capacities of transferring electricity to heat
    p2h_capacities = {}
    for key, value in design_heat_dict.iteritems():
        p2h_capacities[key] = p2h_share * value
        
    #print 'Total P2H capacity', np.sum(p2h_capacities.values()), 'GW'
        
    # now for each region, for each hour, compare the DH demand to the 
    # corresponding p2h capacity. The DH heat demand which can
    # be covered by p2h is found as the minimum value
    # this is named demand_pot (demand potential)
    
    demand_pot = {}
        
    for key, value in county_curves.iteritems():
        demand_pot[key] = np.minimum(value, p2h_capacities[key])
        
    # now calculate the power demanded to supply the heat demand
    P_demand = {}
    
    for key, value in demand_pot.iteritems():
        P_demand[key] = demand_pot[key] * p2h_ratio()
        
    # now, calculate the surplus at every hour where there is a negative power
    # residual 
    P_surplus = np.maximum((-1) * P_res, 0)

    # if there is no accumulation, the result is found by a simple
    # comparison of supply and demand
    if ac_size == 0 or ac_transfer == 0:

        # calculate the hourly total demand
        P_demand_tot = np.sum(P_demand.values(),0)    
    
        # finally, compare the surplus to the demand to get the hourly p2h
        p2h = np.minimum(P_surplus, P_demand_tot)
        
        # and sum up to get the total potential
        p2h_sum = np.sum(p2h)
        
        print 'Total potential:', p2h_sum, 'GWh'
        
        p2ac = 0
        storage = 0
    
    # if there is accumulation potential, simulate how it affects the
    # P2H potential
    else:
    
        # set up accumulators
        acs = {}
        
        for key, value in demand_pot.iteritems():
            q_daily_mean = np.mean(value) * 24
            max_storage = q_daily_mean/4 * ac_size
            acs[key] = Accumulator(max_storage, 0, q_daily_mean/40 *ac_transfer, 
                                    max_storage/2)
        
        # simulate accumulation   
        res = sim_ac(demand_pot, P_surplus, acs)
        p2h = res['p2h']
        storage = res['storage']
        p2ac = res['p2ac']

    # find path of package top folder
    dir_Analysis = os.path.dirname(os.path.abspath(__file__))    
    dir_Modules = os.path.dirname(dir_Analysis)
    
    # specify filename for results    
    
    if type(scenario_nbr) == dict:
        file_name = scenario_nbr['Name']
    else:    
        file_name = 'Scen_{}'.format(scenario_nbr) 
        if ac_size != 0 and ac_transfer != 0:
            file_name += '_size_{}_transfer_{}'.format(ac_size, ac_transfer)
        if exclude_waste:
            file_name += '_ex_waste'
        if hydro_min != -1:
            file_name += '_hydro_min_{}'.format(hydro_min)
        if wind_yr != 2014:
            file_name += '_wind_yr_{}'.format(wind_yr)
        if solar_yr != 2014:
            file_name += '_solar_yr_{}'.format(solar_yr)
        if p2h_share != 0.3:
            file_name += '_cost_opt'
        if power_cons != -1:
            file_name += '_power_cons_{}'.format(power_cons)
        
    # set path for where to store results
    file_location = os.path.join(dir_Modules, 'Results', 'p2h', 
                                 file_name)
                                 
    # save the hourly potential to file
    np.savetxt(file_location, p2h)
    
    # return the results in a dictionary              
    return {'P_res': P_res,
            'county_curves': county_curves,
            'P_demand': P_demand,
            'demand_pot': demand_pot,
            'P_surplus': P_surplus,
            'p2h': p2h,
            'p2ac': p2ac,
            'storage': storage}
    
def sim_pot(scenario, ac_size = 0, ac_transfer = 0, 
            exclude_waste = False, wind_scen = 2014):
    """ Performs all three steps of the simulation process and
    then plots different results. Returns the results in a
    dictionary.
    """        
            
    # calculate hourly power residual
    P_res = power_scen_to_res(scenario)
    
    # calculate DH curves
    county_curves, design_heat_dict = temp_to_heat(exclude_waste)
    
    tic = time.clock()
    
    # simulate power-to-heat potential
    result_dict = sim_p2h(P_res, county_curves, design_heat_dict, 
                          scenario, exclude_waste,
                          ac_size, ac_transfer)
    
    toc = time.clock()
    
    print 'Processing time is', toc - tic, 's'
     
    # make plots and print results               
    plot_results_old(result_dict)
    
    return result_dict
                    
if __name__ == "__main__":
    
    plt.close('all')    
    
    # specify scenario
    scenario = 'High Wind'
    
    #simulate
    sim_pot(scenario)
    