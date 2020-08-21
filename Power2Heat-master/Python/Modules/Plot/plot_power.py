# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:41:17 2016

@author: Jonatan
"""

from __future__ import division
from Modules.Simulate.sim_p2h import power_scen_to_res
from Modules.Power.specify_scenarios_with_export import specify_scenario
from Modules.Power.read_power_data import read_power_data
from Modules.Power.calc_power import calc_power_curves
import matplotlib.pyplot as plt
import numpy as np

def plot_power_res(scen):
    """ Reads scenario numbers and plots the power residuals for these.
    Also prints the sum of negative power residuals for each scenario.
    """
    
    plt.figure(10)
    
    power_res = {}
    
    for s in scen:
        power_res[s] = power_scen_to_res(s)
        
        # now, calculate the surplus at every hour where there is a negative power
        # residual 
        P_surplus = np.maximum((-1) * power_res[s], 0)
        print 'Scen', s, 'P_res_tot', np.sum(P_surplus)
        
        power_res[s][::-1].sort()
#        if s == 0:
#            name = 'Current'
#        else: 
#            name = 'Scen_{}'.format(s)
        name = s
        plt.plot(power_res[s], label = name)
    
    plt.plot(np.zeros(8760), 'k--')
    plt.legend()
    plt.xlabel('Time [h]')
    plt.ylabel('Power residual [GW]')
    plt.show()

def plot_power(scen):
    """ Reads list of scenario names and plots the power over time for 
    different production and consumption"""
    
    for i,s in enumerate(scen):    
    
        scenario_data = specify_scenario(s)
        
        # read power data
        power_data = read_power_data()
        
        # calculate power curves
        power_curves = calc_power_curves(scenario_data, power_data)
        
        # set figure number
        plt.figure(i)        
        
        # set order of plotting by a list of keys
        order = ['Solar', 'Consumption','Hydro', 'Wind', 'Other', 'Nuclear']                
        
        #now plot over time
        for key in order:
            if key == 'Nuclear':
                #plot nuclear in black
                plt.plot(power_curves[key], 'k', label = key)
            else:
                plt.plot(power_curves[key], label = key)

        plt.xlabel('Time [h]')
        plt.ylabel('Power [GW]')
        plt.title('Scenario {}'.format(s))
        plt.legend()
        plt.show()


if __name__ == '__main__':

#    scen = [0, 1, 2, 3, 4]
#    
#    plot_power_res(scen)

    # plot Max's scenarios
    #scen = ['A', 'B', 'C', 'D']

    plt.close('all')

    scen = ['Current', 'Conservative', 'High Wind', 'High Wind & Solar']

    plot_power(scen)
    
    plot_power_res(scen)
        
    