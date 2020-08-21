# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:48:24 2016

@author: Gerald
"""
from __future__ import division
import numpy as np
#import pandas

def calc_heat_curve(T_data, q_tot, T_ex):
    """ Calculates hourly heat data, based on temperature data, total yearly
        heat demand and extreme temperature. Returns a tuple containing the
        hourly heat demand as well as the design heat.
    """

#    Year = pandas.date_range('1/1/2014', periods=8760, freq='H')
#    
#    
#    size = (8760,3)
#    epw = np.zeros(size)
#    k = 0 # counter
#    
#    year= [31,28,31,30,31,30,31,31,30,31,30,31]
#    for ll, months in enumerate(year):
#        for day in range(1, months+1):
#            for hour in range(1,25):
#                  epw[k,0] = ll+1
#                  epw[k,1] = day
#                  epw[k,2] = hour
#                  k=k+1

    if q_tot == 0:
        return 0
    else:
    
        Tmin = T_ex
        Tmax = 15.0 # source?
        
        MaxLoad = 1
        
        # Set the amount of heat that is assumed to be constant throughout
        # the year. This consisits of tap water and distribution losses.
        constant_share = 0.30        
        
        y_upper = constant_share
        y_lower = 0
        
        n_hours = len(T_data)
        
        # iterate for different values of relative MinLoad until the amount of
        # heat used for hot water is 30 percent
        # use bisection method
        while True:
            MinLoad = (y_upper + y_lower)/2           
           
            k = (MinLoad-MaxLoad)/(Tmax -Tmin)
            d = MaxLoad -(Tmin*k)    
            
            Qnorm = np.zeros(len(T_data))
            
            for numel, Temperature in enumerate(T_data):         
                
                if Temperature >= Tmax:
                    Qnorm[numel] = MinLoad
                elif Temperature< Tmin:
                    Qnorm[numel] = MaxLoad
                else:
                    Qnorm[numel] = Temperature*k+d
                          
            Qnorm[np.isnan(Qnorm)] = MinLoad
            
            # calculate the design capacity
            q_design = q_tot/np.sum(Qnorm)
            
            q_final = q_design * Qnorm
            
            # check if the amount of heat used for hot water is close enough to
            # 30 percent
            amount_hot_water = MinLoad * q_design * n_hours / q_tot
            if np.isnan(amount_hot_water):
                print 'Nan'
                print 'MinLoad', MinLoad
                print 'q_tot', q_tot
                print 'q_design', q_design
                break
            
    
            if  np.absolute(amount_hot_water - constant_share) < 10**(-3):
                #print amount_hot_water, 'percent of the heat is used for hot water'
                #print 'MinLoad', MinLoad
                break
            elif amount_hot_water > constant_share:
                y_upper = MinLoad            
            else:
                y_lower = MinLoad
        
        return q_final, q_design

