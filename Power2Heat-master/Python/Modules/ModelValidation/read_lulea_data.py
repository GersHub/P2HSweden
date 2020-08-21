# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 09:15:15 2016

@author: Jonatan
"""
from __future__ import division
import numpy as np
import os

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def read_lulea_data():
    """
    Reads hourly DH data for Luleå in 2011 and 2012 from file.
    """    

    dir_ModelValidation = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_ModelValidation)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    # read data for 2012
    file_location_2012 = os.path.join(dir_Power2Heat, 'Data', 'Validation', 
                                 'MeasuredDataForDHN', 'Lulea', 
                                 'DH_data_Lulea_2012.csv')
    file_2012 = np.genfromtxt(file_location_2012, delimiter = ';', names = True, 
                         dtype = float, usecols = (3, 4))                  
                         
    # read data for 2011
    file_location_2011 = os.path.join(dir_Power2Heat, 'Data', 'Validation', 
                                 'MeasuredDataForDHN', 'Lulea', 
                                 'DH_data_Lulea_2011.csv')
    file_2011 = np.genfromtxt(file_location_2011, delimiter = ';', names = True, 
                         dtype = float, usecols = (3, 4))   
    
    # extract important data and store in a dictionary
    lulea_data = {  '2012': {'q': file_2012['q_tot'],
                             'T': file_2012['Temp_U']},
                    '2011': {'q': file_2011['q_tot'],
                             'T': file_2011['Temp_U']}}

    # replace NaNs
    for yr, data in lulea_data.iteritems():
        for k,v in data.iteritems():            
            nans, x = nan_helper(v)
            v[nans] = np.interp(x(nans), x(~nans), v[~nans])

    return lulea_data


    
    
    
    