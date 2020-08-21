# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:46:44 2016

@author: Jonatan
"""

from __future__ import division
import os
import numpy as np

def rewrite_temp_data():
    """
    reads the hourly temperature data for many years from file for all cities 
    and rewrites it for only 2014
    """

    # specify location of file with county data
    dir_Files_from_Jonatan = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_Files_from_Jonatan)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    dir_Temperatures = os.path.join(dir_Power2Heat, 'Data', 'Temperatures')
    dir_Temperatures2014 = os.path.join(dir_Power2Heat, 'Data', 
                                                        'Temperatures2014')
    
    txt_file_location = os.path.join(dir_Power2Heat, 'Data', 
                                'List of counties and temperature data.csv')
    
    # read data and store in numpy arrays
    file = np.genfromtxt(txt_file_location, delimiter = ';', names = True, 
                                                             dtype = None)
                                                             
    filename_list = file['Data_filename']

    for filename in filename_list:
        # read from file c_dict['data_filename']
        read_file_location = os.path.join(dir_Temperatures, filename)       
        file1 = np.genfromtxt(read_file_location, delimiter = ';', names = True,
                                                      dtype = None)

        dates = file1['Datum']
        hours = file1['Klockslag']
        temps_with_commas = file1['Timmedel']
        temps = []
        for t in temps_with_commas:
            temps.append(float(t.replace(',', '.')))
        
        
        # find the start and end indices for the 2014 data
        # this could be done faster with a different search algorithm!
        for index, date in enumerate(dates):
            if date == '2014-01-01' and hours[index] == '00:00:00':
                start_index = index
                print 'reading data for', filename
            if date == '2014-12-31' and hours[index] == '23:00:00':
                end_index = index
                #print index
                break
            
        # control that the number of hours is correct
        if end_index - start_index + 1 != 365*24:
            raise Exception('Wrong number of hours!')
        
        # specify location of file to write to
        write_file_location = os.path.join(dir_Temperatures2014, filename)        
        
        np.savetxt(write_file_location, temps[start_index: end_index + 1])

        
if __name__ == '__main__':
    temp_dict = rewrite_temp_data()
                    
