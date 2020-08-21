# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 09:13:08 2016

@author: Jonatan
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import os
    
def plot_compare_sup_dem(P_res, q_tot, xplanation, fig_nbr = 1, 
                                                 set_axis = False):
    """ Compare the P2H supply and demand.
    """

    plt.figure(fig_nbr)
    
    # define array in order to plot a line where DH demand is equal to negative
    # power residual
    x_balance_line = np.array(range(int(round(max(q_tot)))))
    y_balance_line = (-1) * x_balance_line
    xaxis = range(int(np.ceil(max(q_tot))) + 1)
    
    plt.plot(xaxis, np.zeros(len(xaxis)), '--')
    plt.plot(q_tot, P_res, '.')
    plt.plot(x_balance_line, y_balance_line)
    
    plt.xlabel(xplanation)
    plt.ylabel('Residual Power Load [GW_el]')
    
    if set_axis:
        plt.xlim(0,18)
        
def plot_p2h_over_time(p2h):
    """ Plot the hourly p2h chronologically.
    """
    
    
def plot_compare_scenarios(p2h, plot_name):
    """ Plot the hourly p2h in descending order for the different scenarios.
    """
    
    dir_name = os.path.dirname(os.path.abspath(__file__))
    dir_Python = os.path.dirname(os.path.dirname(dir_name))
    
    plt.figure(8)
    plt.clf()
    
#    # set the plotting order manually
#    plot_order = ['Conservative', 'High Wind', 'High Wind & Solar']
#    
#    if 'Current' in p2h:
#        plot_order.insert(0,'Current')
#    
##    for key, value in p2h.iteritems():
#    for key in plot_order:
#        
#        value = p2h[key]
        
    for key, value in p2h.iteritems():
        #delete the zero values
        surplus_values = value[value != 0]        
        
        #sort the p2h values in descending order
        surplus_values[::-1].sort()            
        #plt.plot(surplus_values, label = 'Scen_{}'.format(key))
        plt.plot(surplus_values, label = key)
        
    plt.legend()
    plt.xlabel('Hours with negative residual load')
    plt.ylabel('Simulated P2H potential [GW_el]')
    
    plt.savefig(os.path.join(dir_Python, 'Plots', '{}.png'.format(plot_name)))