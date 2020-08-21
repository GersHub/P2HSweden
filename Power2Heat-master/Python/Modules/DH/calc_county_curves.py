# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:02:04 2016

@author: Gerald
"""
from calc_heat_curve import calc_heat_curve

def calc_county_curves(temp_dict, heat_dict, exclude_waste):
    """ returns a tuple containing two dictionaries. The first dictionary maps
        counties to lists with hourly DH demand values. The second
        dictionary maps counties to design heat loads.
    """ 
    print 'Calculating regional heat curves'    
    
    # first calculate the total heat load and the total waste heat
    # for each region
    
    q_tot = {}
    waste_tot = {}    
    
    for key, value in heat_dict.iteritems():
        if value[0] not in q_tot:
            q_tot[value[0]] = value[1]
        else:
            q_tot[value[0]] += value[1]
        
        if value[0] not in waste_tot:
            waste_tot[value[0]] = value[2]
        else:
            waste_tot[value[0]] += value[2]
    
    # Create dictionaries in which to store the heat curves and
    # the design heat loads
    heat_curves = {}
    design_heat_dict = {}    
    
    # iterate over counties in temperature data
    # for each one calculate the hourly heat demand, at this stage
    # including the waste heat
    for key, value in temp_dict.iteritems():
        heat_curves[key], design_heat_dict[key] = calc_heat_curve(
                        value['data_list'], q_tot[key], value['T_ext'])

    if exclude_waste:    
        # now extract the waste heat, if applicable
        for key, value in heat_curves.iteritems():
            # first check if it's possible to distribute the waste heat evenly
            # over all values
        
            # make a list of lists coupling time index and corresponding heat
            # demand        
            heat_list = [[t, q] for t, q in enumerate(value)]
            
            # sort the list according to heat
            heat_list.sort(key=lambda x: x[1])
    
            # store the waste heat to be distributed in a local variable
            rem_heat = waste_tot[key]
    
            # calc total heat up to next min value
            heat_block = heat_list[0][1] * len(heat_list)        
            
            while rem_heat > heat_block:
                for h in heat_list:
                    # remove heat from sorted list
                    h[1] -= heat_list[0][1]
                    # remove heat from actual list
                    value[h[0]] -= heat_list[0][1]
                rem_heat -= heat_block
                heat_list.pop(0)
                heat_block = heat_list[0][1] * len(heat_list)  
            
            for h in heat_list:
                value[h[0]] -= heat_block/len(heat_list)
            
                        
#    # now go back to the final format mapping cities to hourly q and county
#    heat_cities = {}
#    for key, value in heat_dict.iteritems():
#        heat_cities[key] = {'q_hourly': heat_curves[value[0]]*value[1]/q_tot[value[0]],
#                            'county': value[0]}
                            
    return heat_curves, design_heat_dict