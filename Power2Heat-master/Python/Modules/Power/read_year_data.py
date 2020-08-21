# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import os
from Modules.ModelValidation.read_Kraftringen_data import lin_int_nan

def read_wind_data():
    return read_year_data('Wind_data.csv')
    
def read_solar_data():
    return read_year_data('Solar_data.csv')

def read_year_data(filename):
    """
    Reads hourly power data (in MW) for Swedish production for different
    years from fileThe data is returned in a dictionary.
    """    

    dir_Power = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_Power)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    file_location = os.path.join(dir_Power2Heat, 'Data', filename)
    file1 = np.genfromtxt(file_location, delimiter = ';', names = True, dtype = float)        
    
    
    year_dict = {2011: file1['2011'], 
                 2012: file1['2012'], 
                 2013: file1['2013'], 
                 2014: file1['2014'], 
                 2015: file1['2015']}
                 
    for key, value in year_dict.iteritems():
        value = lin_int_nan(value)
    
    return year_dict
    
    



