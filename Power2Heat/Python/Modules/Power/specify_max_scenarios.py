# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:11:06 2016

@author: Jonatan
"""

def specify_scenario(scenario):
    """ Returns a dictionary containing the yearly total energy in TWh for
    consumption and for different types of production
    """
    
    P_dict = {}    
    
    if scenario == 'A':
        P_dict["Nuclear"] = 0
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 100
        P_dict["Solar"] = 95
        P_dict["Consumption"] = 275
    
    elif scenario == 'B':
        P_dict["Nuclear"] = 60
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 20
        P_dict["Solar"] = 0
        P_dict["Consumption"] = 160
        
    elif scenario == 'C':
        
        P_dict["Nuclear"] = 0
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 64
        P_dict["Solar"] = 0
        P_dict["Consumption"] = 144  
        
    elif scenario == 'D':
        
        P_dict["Nuclear"] = 0
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 64
        P_dict["Solar"] = 50
        P_dict["Consumption"] = 194  
        
    return P_dict
    