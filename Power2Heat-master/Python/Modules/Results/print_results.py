# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:47:43 2016

@author: Jonatan
"""

from __future__ import division
import os
from Modules.Power.calc_power import p2h_ratio

def print_results(scenario_nbr, P_tot, q_tot, p2h, ac_pot, p2h_with_ac, 
                  p2ac, ac_size, ac_transfer):
    """Prints the simulation settings and results to file
    """
    
    dir_Results = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(dir_Results, 
                    'Scen_{0}_ac_size_{1:.2f}_ac_transfer_{2:.2f}.txt'.format(
                    scenario_nbr, ac_size, ac_transfer))
    
    f = open(file_dir, 'w')
    f.write('Settings\n')
    f.write('Scenario: \t %.0f \n' % (scenario_nbr))
    f.write('Accumulator size factor: {}'.format(ac_size) )
    
    f.write('Results\n')
    f.write('Total Power Residual: \t\t\t %.0f GWh_el\n' % (P_tot))
    f.write('Total yearly DH heat demand: \t\t %.0f GWh_th\n\n' % (q_tot))
    l = 'P2H potential without accumulation:' + \
        '\t {0:.0f} GWh_el ({1:.0f} GWh_th)\n'
    f.write(l.format(p2h, p2h / p2h_ratio()))
    #f.write('Theoretical Accumulation potential:\t %.0f \tGW_el\n' % (ac_pot))    
    #f.write('Power used for accumulating heat:\t %.0f \tGW_el\n' % (p2ac))
    l = 'P2H potential with accumulation:' + \
        '\t {0:.0f} GWh_el ({1:.0f} GWh_th)'
    f.write(l.format((p2h_with_ac), p2h_with_ac / p2h_ratio()))

if __name__ == "__main__":
    print_results(1, 2, 3, 4, 5, 6, 7)