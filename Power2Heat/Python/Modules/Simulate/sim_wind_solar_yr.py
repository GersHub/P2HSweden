# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 13:52:54 2016

@author: Jonatan

simulate for different wind profiles
"""

from __future__ import division
from sim_p2h import temp_to_heat, sim_p2h
from Modules.Power.specify_scenarios_with_export import specify_scenario
from Modules.Power.read_power_data import read_power_data
from Modules.Power.read_year_data import read_year_data
from Modules.Power.calc_power import calc_power_curves, calc_power_residual

scen = ['Conservative', 'High Wind', 'High Wind & Solar']

# specify wind or solar
source = 'Solar'

# specify filename based on source
if source == 'Wind':
    filename = 'Wind_data.csv'
elif source == 'Solar':
    filename = 'Solar_data.csv'
else:
    raise Exception('Only sources available are Wind and Solar!')

yrs = [2011, 2012, 2013, 2014, 2015]

cc, dhd = temp_to_heat()

for s in scen:
    for y in yrs:
        scenario_data = specify_scenario(s)
        power_data = read_power_data()
        
        # if specified, choose wind curve to use
        if y != 2014:
            yr_dict = read_year_data(filename)
            # for 2012 exclude the last day of the year, in order to get
            # 365 days
            power_data[source] = yr_dict[y][:8760]
        
        power_curves = calc_power_curves(scenario_data, power_data)
        P_res = calc_power_residual(power_curves, hydro_min = 1.682)
        
        if source == 'Wind':
            result = sim_p2h(P_res, cc, dhd, s, wind_yr = y)
        else:
            result = sim_p2h(P_res, cc, dhd, s, solar_yr = y)