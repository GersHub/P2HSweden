# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:57:55 2016

@author: Jonatan
"""

from __future__ import division
import os
import numpy as np    
import copy

def read_temp_data():
    """
    reads the 2014 hourly temperature data from file for all cities 
    and returns a dictionary which maps counties to dictionaries containing
    extreme temperatures and hourly temperature data.
    """

    # specify location of file with county data
    dir_Files_from_Jonatan = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_Files_from_Jonatan)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    dir_Temperatures2014 = os.path.join(dir_Power2Heat, 'Data', 'Temperatures2014')
    
    txt_file_location = os.path.join(dir_Power2Heat, 'Data', 
                                'List of counties and temperature data.csv')
    
    # read data and store in numpy arrays
    file = np.genfromtxt(txt_file_location, delimiter = ';', names = True, 
                                                             dtype = None)
                                                             
    county_list = file['County']
    filename_list = file['Data_filename']
    extreme_temp_list = file['Extreme_outdoor_temperature']
    
    # store values in a dictionary with counties as keys and a list with
    # data filename and extreme outdoor temperature as value
    counties = {}
    for i, c in enumerate(county_list):
        counties[c] = {'T_ext':extreme_temp_list[i], 'data_filename':filename_list[i]}

    for c, c_dict in counties.iteritems():
        # specify file location
        txt_file_location = os.path.join(dir_Temperatures2014, c_dict['data_filename'])
        print 'Loading data for:', c
        # load data from file
        c_dict['data_list'] = np.loadtxt(txt_file_location)
        
    #check for nan    
    counties1=copy.deepcopy(counties)   # need deecopy --> otherwise not "real" copy off whole list
    numberNan = []
    numberNanAfter = []
    #new_array = remove_nans(old_array)
    for i, ii in enumerate(counties1):
        dataWithoutNan = np.array(counties1[ii]["data_list"])
        mask = np.isnan(counties1[ii]["data_list"])
        numberNan.append("{} has {} nan".format(ii,sum(mask)))
        dataWithoutNan[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), dataWithoutNan[~mask])
        counties1[ii]["data_list"] = dataWithoutNan
        mask1 = np.isnan(counties1[ii]["data_list"])
        numberNanAfter.append("{} has {} nan".format(ii,sum(mask1)))
       
#    back = []
#    back.append(counties)
#    back.append(counties1) 
#    back.append(numberNan)
#    back.append(numberNanAfter) # check if everywhere are zero NAN values
    
    return counties1
    
if __name__ == '__main__':
    temp_dict = read_temp_data()
                    
