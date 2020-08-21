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
    
def lin_int_nan(v):
    """ For the array v, make linear interpolation for nans and return the 
    result
    """
    nans, x = nan_helper(v)
    v[nans] = np.interp(x(nans), x(~nans), v[~nans])
    
    return v


def read_Kraftringen_data():
    """
    Reads hourly DH data for Lund, Lomma and Eslöv in 2014 from file.
    """    

    dir_ModelValidation = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_ModelValidation)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    file_location = os.path.join(dir_Power2Heat, 'Data', 'Kraftringen_data_2014.csv')
    file = np.genfromtxt(file_location, delimiter = ';', names = True, 
                         dtype = float, usecols = (1, 2, 3, 4, 5))                          
    
    # extract important data and store in a dictionary
    kraftringen_data = {'lund': file["Lund"],
                        'lomma': file['Lomma'],
                        'eslov': file['Eslov'],
                        'T': file['Outdoor_temp'],
                        'Total': file['Total']}    

    # replace NaNs
    for k, v in kraftringen_data.iteritems():
        v = lin_int_nan(v)

    return kraftringen_data


    
    
    
    