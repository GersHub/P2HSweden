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
    
    if scenario == 'Current':
        P_dict["Nuclear"] = 54.2
        P_dict["Hydro"] = 74.3
        P_dict["Other"] = 13.4
        P_dict["Wind"] =16.3
        P_dict["Solar"] = 0.01
        P_dict["Consumption"] = 135.5
    
    elif scenario == 'Conservative':
        P_dict["Nuclear"] = 55
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 30
        P_dict["Solar"] = 5
        P_dict["Consumption"] = 140 #175 #140
        
    elif scenario == 'High Wind':
        
        P_dict["Nuclear"] = 0
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 70
        P_dict["Solar"] = 5
        P_dict["Consumption"] = 140 #155 #140
        
    elif scenario == 'High Wind & Solar':
        
        P_dict["Nuclear"] = 0
        P_dict["Hydro"] = 65
        P_dict["Other"] = 15
        P_dict["Wind"] = 70
        P_dict["Solar"] = 20
        P_dict["Consumption"] = 140 #170 #140
    
#    # add a value of the import/export, which is assumed to be equal to
#    # the difference between production and consumption
#    prod_tot = sum(P_dict.values()) - P_dict["Consumption"]
#    P_dict["Export"] = prod_tot -  P_dict["Consumption"]
#    
#    #print 'Total Export for scenario {}:'.format(scenario), P_dict["Export"]
        
    return P_dict
    