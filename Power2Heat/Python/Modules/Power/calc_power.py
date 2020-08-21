# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:26:31 2016

@author: Jonatan
"""

from __future__ import division
import numpy as np

def p2h_ratio(COP = 2, hp_share = 0):
    """ Returns the ratio between power and heat for given hp_share and COP.
    """
    return 1/((COP -1)*hp_share + 1)

def calc_power_curves(scenario_data, power_data):
    """ Based on the scenario specification and the power data calculates
        a power curve (in GW) for the scenario.
    """

    power_templates = {}
  
    # first normalize the power data
    for key, p in power_data.iteritems():
        
        # there is no need to include the total production curve,
        # since we instead want to make curves for the individual
        # power types
        if key != 'Production':            
        
            # calculate the total amount of production
            p_tot = sum(p)
            
            # p is in MW, p_tot is in MWh
            #in order oto get a normalized curve, correspnding to a yearly total
            # production of 1 TWh, multiply each value with 1000000/wind_tot
            
            p_normalized = 1000000/p_tot * p
            
            # Now the values are in MW, but in order to get it in GW we divide by 1000
            power_templates[key] = p_normalized/1000
    
    power_curves = {}
    
    if 'Export' not in scenario_data:
        scenario_data['Export'] = 0   
    
    for key, p in power_templates.iteritems():        
        power_curves[key] = p * scenario_data[key]        
 
    # multiplying with the factor 1000 is done in order to convert TWh to GWh    
#    power_curves['Export'] = scenario_data['Export'] * 1000 /(356*24) * \
#                                np.ones(365 * 24)
    
    return power_curves
    
def calc_power_residual(power_curves, th_res = 0.5, hydro_min = 1.682):
    """ Based on the hourly power curves, and the definition 'def_res' of which
    production to be included, calculate the hourly power residual.
    """
        
    P_prod =    power_curves['Wind'] + power_curves['Solar'] + \
                np.mean(power_curves['Nuclear']) + \
                th_res * power_curves['Other'] + \
                hydro_min
            
    #print 'power curve Export', power_curves['Export'] 
            
    # Accounting for export        
    #P_res = power_curves["Consumption"] + power_curves['Export'] - P_prod
            
    # Excluding export
    P_res = power_curves["Consumption"] - P_prod
    
    return P_res