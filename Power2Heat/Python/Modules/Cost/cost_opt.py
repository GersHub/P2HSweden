# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 08:44:10 2016

@author: Jonatan
"""

from __future__ import division
import numpy as np
import os
import math
import matplotlib.pyplot as plt

def optimize_capacity(scenario):
    
    dir_Cost = os.path.dirname(os.path.abspath(__file__))    
    dir_Modules = os.path.dirname(dir_Cost)
    
    # specify location of results
    file_location = os.path.join(dir_Modules, 'Results', 'p2h', 
                                 'Scen_{}'.format(scenario))
    
    # read results and store technical potential in numpy array
    tech_p2h = np.loadtxt(file_location)
    
    # calculate optimal investment
    P_installed = cost_opt(tech_p2h)
    
    print 'optimal amount of P_installed is', P_installed
    
    return P_installed

def annualize(investment):
    """ Calculates the annualized investment cost [SEK] of electric boilers
    based on level of installed power P [GW].
    """    
    
    # Expected lifetime 20 years
    # http://www.energinet.dk/SiteCollectionDocuments/Danske%20dokumenter/Forskning/Technology_data_for_energy_plants.pdf
    # p. 122
    # longer expected lifetime because of the limited time being in use?
    # or shorter because of being switched on and off frequently?
    t = 20 
    
    # interest rate
    # Elforsk-rapport s. vii, http://www.elforsk.se/Rapporter/?rid=14_40_
    r = 0.06    # alternative 0.07?
    
    # calculate Equivalent Annual Cost in MSEK/GW
    # Wikipedia: Equivalent Annual Cost
    EAC = investment /((1 - 1/(1 + r)**t)/r)
    
    return EAC
    

def capacity_to_heat(p, p2h_sorted_pot):
    """ Calculates the heat that can be provided by P2H, 
    based on the sorthed hourly P2H potential and the installed power p.
    NOTE: This is a heuristic method which will give approximately the right
    value, but it may be a bit higher than the actual, since in reality
    the capacity limits are at the local level rather than the national.
    """
    
    # Compare the hourly p2h potential with the p2h capacity,
    # the minimum gives the actual hourly potential
    
    p2h = np.minimum(p, p2h_sorted_pot)
    
    # now the heat we can produce can be calculated as the sum
    # of the hourly p2h potentials    
    
    return np.sum(p2h)

def calc_profit(P, q_heat):
    
    # set heat price [MSEK/GWh]
    # http://www.energimyndigheten.se/globalassets/nyheter/2013/tradbransle-och-torvpriser-en0307_sm1304.pdf
    p_heat = 0.2
    # medel fjärrvärme 0.4?? Patrick källa!
    
    # set electricity price [MSEK/GWh]
    p_el = 0
    
    # boiler costs  
    # http://www.energinet.dk/SiteCollectionDocuments/Danske%20dokumenter/Forskning/Technology_data_for_energy_plants.pdf
    # Technology data for energy plants, p.20
    investment = 0.06   # [M€/ MW]
    fixed_om = 1100    # [€/MW/yr]
    var_om = 0.5       # [€/MWh]
    
    # set exchange rate from € to SEK
    ex_rate = 9.2  # [SEK/€]
    
    # in order to go from [M€/MW] to [MSEK/GW] we need to multiply by
    # ex_rate * 1000
    investment = investment * ex_rate * 1000   
    # in order to go from [€/MW/yr] to [MSEK/GW/yr] we need to multiply by
    # ex_rate * 1000 /10^6
    fixed_om = fixed_om * ex_rate * 1000 /10**6
    # in order to go from [€/MWh] to [MSEK/GWh] we need to multiply by
    # ex_rate *1000 /10^6
    var_om = var_om * ex_rate * 1000 /10**6   
    
    EAC = annualize(investment)
    
    # calculate and print annualized investment cost for electric boilers
    #print "Specific Annualized investment cost:", EAC, "[MSEK/GW]"    
    
    # first calculate the investment cost
    c_inv = EAC * P
    
    # calculate the fixed operations and maintenance costs
    c_fixed_om = fixed_om * P
    
    # calculate the variable operations and maintanence costs
    c_var_om = var_om * q_heat
    
    # for now assume electric boilers with a hundred percent efficiency
    q_el = q_heat    
    
    # evalueate the objective function    
    profit = q_heat * p_heat - q_el * p_el - \
                c_inv - c_fixed_om - c_var_om
                
    income = q_heat * p_heat
                
    return {'c_inv': c_inv,
            'c_fixed_om': c_fixed_om,
            'c_var_om': c_var_om,
            'profit': profit,
            'income': income}

def cost_opt(p2h_pot):
    """ Calculates the optimal amount of electric boilers to invest in
    (P_installed), based on  
    heat price and electricity price (possibly including taxes).
    
    The third inparameter is the hourly P2H potentials, which are used to
    calculate the total P2H potential based on the hourly P2H capacity.
    """
    ### try brute force =) 
    
    # sort the p2h potentials in descending order
    p2h_sorted_pot = np.sort(p2h_pot)[::-1]
    
    # first find the maximal p2h potential
    P_max = p2h_sorted_pot[0]
    
    # make a numpy array ranging all integer numbers between zero and P_max
    # rounded up to the nearest integer
    P = np.linspace(0, int(math.ceil(P_max)) + 1, num = 251)
    
    # calculate the amount of heat that can be provided
    q_heat = np.array([capacity_to_heat(p, p2h_sorted_pot) for p in P]) 
    
    ### now calculate the profit for all these values
    results = calc_profit(P, q_heat)
        
    plt.plot(P, results['c_inv'], label = 'Investment cost')
    plt.plot(P, results['c_fixed_om'] + results['c_var_om'], label = 'O&M cost')
    plt.plot(P, results['income'], label= 'Income saved fuel')
    plt.plot(P, results['profit'], label = 'Profit')
    plt.plot(P, np.zeros(len(P)), 'k--')
    plt.legend(labelspacing = 0.1)
    plt.ylabel('Value [MSEK]')
    plt.xlabel('Installed power [GW]')
    plt.show()
    
    # now find the index of the maximum profit
    max_ind = np.argmax(results['profit'])
    
    #print 'Estimated amount of heat is', q_heat[max_ind], 'GWh'
    
    # print the maximum profit
    #print 'Maximum profit is:', results['profit'][max_ind], 'MSEK'
    
    # the optimal level of installed power is now returned
    
    return P[max_ind]
    
if __name__ == "__main__":    
    
    # select a power scenario
    scenario = 'High Wind'
    
    optimize_capacity(scenario)