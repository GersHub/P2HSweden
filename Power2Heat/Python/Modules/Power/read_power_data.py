# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import os

def read_power_data():
    """
    Reads hourly power data (in MW) for Sweden in 2014 from file, both for wind 
    production, total production and total consumption. The data is returned 
    in a dictionary.
    """    

    dir_Power = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_Power)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    file_location = os.path.join(dir_Power2Heat, 'Data', 'Power_data_2014.csv')
    file1 = np.genfromtxt(file_location, delimiter = ';', names = True, dtype = None)        
        

    prod_data =  file1['Total_produktion']
    cons_data_negative = file1['Total_foorbrukning']   
    
    # work with positive signs for the consumption:
    cons_data = (-1) * cons_data_negative
    hydro = file1['Vattenkraft']    
    nuclear = file1['Nuclear']        
    pv = file1['Solkraft']    
    imp = file1["Import"] 
    wind = file1['Vindkraft']
    other = file1['ChP']
    
    power_dict = {'Production': prod_data, 'Consumption': cons_data, 
                  'Wind': wind, "Solar": pv, "Nuclear":nuclear,"Hydro": hydro, 
                  'Export': (-1) * imp, "Other": other }
    
    return power_dict
    
if __file__ == '__main__':
    
    power_dict = read_power_data()
    print 'hello'
    print 'Mean hydro is', np.mean(power_dict['Hydro']), 'GW'
    
    



