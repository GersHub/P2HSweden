# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 13:19:37 2016

@author: Jonatan

make comparison of wind data
"""

from __future__ import division
from read_year_data import read_year_data
import matplotlib.pyplot as plt
from read_power_data import read_power_data
import numpy as np

def plot_yrs(filename):        

    yr_dict = read_year_data(filename)
    
    # calc normalized profiles for all years
    rel_power = {}
    
    for key, value in yr_dict.iteritems():
        rel_power[key] = value/sum(value)*1000
    
    # plot wind profiles over time
    plt.clf()

    # store key order in list
    keys = [2015, 2014, 2013, 2012, 2011]    
    #keys = [2015, 2011]    
    
    for key in keys:
        # sort relative wind productions by production
        #value[::-1].sort()
        plt.plot(yr_dict[key], label = key)
        
    plt.legend()
    plt.xlabel('Hours with highest production')
    plt.ylabel('Hourly Power/ Total Yearly Production [GW/TWh]')
    
if __name__ == '__main__':

    # possible filenames:
    # Export_data.csv
    # Solar_data.csv
    # Wind_data.csv    
    
    plot_yrs('Wind_data.csv')






## check for hydro
#power_dict = read_power_data()
#min_hydro = np.min(power_dict['Hydro'])
#
#print 'Min hydro in 2014:', min_hydro, 'MW'
#
## set the total hydro according to the scenarios in TWh
#tot_hydro = 65
#
## calculate mean hydro production in MW
#mean_hydro = 65000000/365/24
#
#print 'Mean hydro is', mean_hydro, 'MW'
#print 'Min compared to mean', min_hydro/mean_hydro